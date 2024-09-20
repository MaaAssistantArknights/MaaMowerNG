import json
import os
from datetime import datetime, timedelta

from evalidate import Expr

from arknights_mower.solvers.base_schedule import BaseSchedulerSolver
from arknights_mower.solvers.reclamation_algorithm import ReclamationAlgorithm
from arknights_mower.solvers.secret_front import SecretFront
from arknights_mower.utils import config, path, rapidocr
from arknights_mower.utils.csleep import MowerExit
from arknights_mower.utils.datetime import format_time
from arknights_mower.utils.depot import 创建csv, 创建json
from arknights_mower.utils.device.adb_client.session import Session
from arknights_mower.utils.device.scrcpy import Scrcpy
from arknights_mower.utils.email import send_message, task_template
from arknights_mower.utils.log import logger
from arknights_mower.utils.logic_expression import get_logic_exp
from arknights_mower.utils.path import get_path
from arknights_mower.utils.plan import Plan, PlanConfig, Room
from arknights_mower.utils.simulator import restart_simulator

base_scheduler = None
operators = config.operators


# 执行自动排班
def main():
    logger.info("开始运行Mower")
    rapidocr.initialize_ocr()
    simulate()


def initialize(
    tasks: list, scheduler: BaseSchedulerSolver | None = None
) -> BaseSchedulerSolver:
    if scheduler:
        scheduler.handle_error(True)
        return scheduler

    base_scheduler = BaseSchedulerSolver()
    plan1 = {}
    plan = config.plan.model_dump(exclude_none=True)
    conf = config.conf
    plan_config = PlanConfig(
        rest_in_full=config.plan.conf.rest_in_full,
        exhaust_require=config.plan.conf.exhaust_require,
        resting_priority=config.plan.conf.resting_priority,
        ling_xi=config.plan.conf.ling_xi,
        workaholic=config.plan.conf.workaholic,
        max_resting_count=config.plan.conf.max_resting_count,
        free_blacklist=conf.free_blacklist,
        resting_threshold=conf.resting_threshold,
        refresh_trading_config=config.plan.conf.refresh_trading,
        free_room=conf.free_room,
    )
    for room, obj in plan[plan["default"]].items():
        plan1[room] = [
            Room(op["agent"], op["group"], op["replacement"]) for op in obj["plans"]
        ]
    # 默认任务
    plan["default_plan"] = Plan(plan1, plan_config)
    # 备用自定义任务
    backup_plans: list[Plan] = []

    for i in plan["backup_plans"]:
        backup_plan: dict[str, Room] = {}
        for room, obj in i["plan"].items():
            backup_plan[room] = [
                Room(op["agent"], op["group"], op["replacement"]) for op in obj["plans"]
            ]
        backup_config = PlanConfig(
            i["conf"]["rest_in_full"],
            i["conf"]["exhaust_require"],
            i["conf"]["resting_priority"],
            ling_xi=i["conf"]["ling_xi"],
            workaholic=i["conf"]["workaholic"],
            max_resting_count=i["conf"]["max_resting_count"],
            free_blacklist=i["conf"]["free_blacklist"],
            resting_threshold=conf.resting_threshold,
            refresh_trading_config=i["conf"]["refresh_trading"],
            free_room=conf.free_room,
        )
        backup_trigger = get_logic_exp(i["trigger"]) if "trigger" in i else None
        backup_task = i.get("task")
        backup_trigger_timing = i.get("trigger_timing")
        backup_plans.append(
            Plan(
                backup_plan,
                backup_config,
                trigger=backup_trigger,
                task=backup_task,
                trigger_timing=backup_trigger_timing,
            )
        )
    plan["backup_plans"] = backup_plans

    logger.debug(plan)
    base_scheduler.global_plan = plan
    base_scheduler.tasks = tasks
    base_scheduler.enable_party = conf.enable_party == 1  # 是否使用线索
    base_scheduler.leifeng_mode = conf.leifeng_mode == 1  # 是否有额外线索就送出
    # 干员宿舍回复阈值
    # 高效组心情低于 UpperLimit  * 阈值 (向下取整)的时候才会会安排休息
    base_scheduler.last_room = ""
    # logger.info("宿舍黑名单：" + str(plan_config.free_blacklist))
    # 估计没用了
    base_scheduler.MAA = None
    base_scheduler.error = False
    base_scheduler.drone_room = None if conf.drone_room == "" else conf.drone_room
    base_scheduler.reload_room = list(
        filter(None, conf.reload_room.replace("，", ",").split(","))
    )

    # 关闭游戏次数计数器
    base_scheduler.task_count = 0

    return base_scheduler


def simulate():
    """
    具体调用方法可见各个函数的参数说明
    """
    logger.info(f"正在使用全局配置空间: {path.global_space}")
    tasks = []
    reconnect_max_tries = 10
    reconnect_tries = 0
    global base_scheduler
    success = False
    while not success:
        try:
            base_scheduler = initialize(tasks)
            success = True
        except MowerExit:
            return
        except Exception as e:
            logger.exception(e)
            reconnect_tries += 1
            if reconnect_tries < 3:
                restart_simulator()
                config.device.client.check_server_alive()
                Session().connect()
                if config.conf.droidcast.enable:
                    config.device.start_droidcast()
                if config.conf.touch_method == "scrcpy":
                    config.device.control.scrcpy = Scrcpy(config.device.client)
                continue
            else:
                raise e
    # base_scheduler.仓库扫描() #别删了 方便我找
    validation_msg = base_scheduler.initialize_operators()
    if validation_msg is not None:
        logger.error(validation_msg)
        return
    if operators != {}:
        for k, v in operators.items():
            if (
                k in base_scheduler.op_data.operators
                and not base_scheduler.op_data.operators[k].room.startswith("dorm")
            ):
                # 只复制心情数据
                base_scheduler.op_data.operators[k].mood = v.mood
                base_scheduler.op_data.operators[k].time_stamp = v.time_stamp
                base_scheduler.op_data.operators[k].depletion_rate = v.depletion_rate
                base_scheduler.op_data.operators[k].current_room = v.current_room
                base_scheduler.op_data.operators[k].current_index = v.current_index
    timezone_offset = 0

    if len(base_scheduler.op_data.backup_plans) > 0:
        conditions = base_scheduler.op_data.generate_conditions(
            len(base_scheduler.op_data.backup_plans)
        )
        for con in conditions:
            validation_msg = base_scheduler.op_data.swap_plan(con, True)
            if validation_msg is not None:
                logger.error(f"替换排班验证错误：{validation_msg}, 附表条件为 {con}")
                return
        base_scheduler.op_data.swap_plan(
            [False] * len(base_scheduler.op_data.backup_plans), True
        )
    while True:
        try:
            if len(base_scheduler.tasks) > 0:
                (base_scheduler.tasks.sort(key=lambda x: x.time, reverse=False))
                logger.info("||".join([str(t) for t in base_scheduler.tasks]))
                remaining_time = (
                    base_scheduler.tasks[0].time - datetime.now()
                ).total_seconds()

                if remaining_time > 540:
                    # 刷新时间以鹰历为准
                    if (
                        base_scheduler.sign_in
                        < (datetime.now() - timedelta(hours=4)).date()
                    ):
                        if base_scheduler.sign_in_plan_solver():
                            base_scheduler.sign_in = (
                                datetime.now() - timedelta(hours=4)
                            ).date()

                    if (
                        base_scheduler.daily_visit_friend
                        < (datetime.now() - timedelta(hours=4)).date()
                    ):
                        if base_scheduler.visit_friend_plan_solver():
                            base_scheduler.daily_visit_friend = (
                                datetime.now() - timedelta(hours=4)
                            ).date()

                    if (
                        base_scheduler.daily_report
                        < (datetime.now() - timedelta(hours=4)).date()
                    ):
                        if base_scheduler.report_plan_solver():
                            base_scheduler.daily_report = (
                                datetime.now() - timedelta(hours=4)
                            ).date()

                    if (
                        config.conf.skland_enable
                        and base_scheduler.daily_skland
                        < (datetime.now() - timedelta(hours=4)).date()
                    ):
                        if base_scheduler.skland_plan_solover():
                            base_scheduler.daily_skland = (
                                datetime.now() - timedelta(hours=4)
                            ).date()

                    if (
                        config.conf.check_mail_enable
                        and base_scheduler.daily_mail
                        < (datetime.now() - timedelta(hours=8)).date()
                    ):
                        if base_scheduler.mail_plan_solver():
                            base_scheduler.daily_mail = (
                                datetime.now() - timedelta(hours=8)
                            ).date()

                    if config.conf.recruit_enable:
                        base_scheduler.recruit_plan_solver()

                    # 应该在maa任务之后
                    def _is_depotscan():
                        import pandas as pd

                        path = get_path("@app/tmp/depotresult.csv")
                        if os.path.exists(path):
                            depotinfo = pd.read_csv(path)
                            仓库识别时间戳 = depotinfo.iloc[-1, 0]
                            return int(仓库识别时间戳)
                        else:
                            logger.info(f"{path} 不存在,新建一个存储仓库物品的csv")
                            now_time = (
                                int(datetime.now().timestamp())
                                - config.conf.maa_gap * 3600
                            )
                            创建csv()
                            创建json()
                            return now_time

                    if config.conf.maa_depot_enable:
                        dt = int(datetime.now().timestamp()) - _is_depotscan()
                        if dt >= config.conf.maa_gap * 3600:
                            base_scheduler.仓库扫描()
                        else:
                            logger.info(
                                f"仓库扫描未到时间，将在 {config.conf.maa_gap - dt // 3600}小时之内开始扫描"
                            )
                    if config.conf.maa_enable == 1:
                        subject = f"下次任务在{base_scheduler.tasks[0].time.strftime('%H:%M:%S')}"
                        context = f"下一次任务:{base_scheduler.tasks[0].plan}"
                        logger.info(context)
                        logger.info(subject)
                        body = task_template.render(
                            tasks=[
                                obj.format(timezone_offset)
                                for obj in base_scheduler.tasks
                            ],
                            base_scheduler=base_scheduler,
                        )
                        send_message(body, subject)
                        base_scheduler.maa_plan_solver()
                    else:
                        remaining_time = (
                            base_scheduler.tasks[0].time - datetime.now()
                        ).total_seconds()
                        subject = f"休息 {format_time(remaining_time)}，到{base_scheduler.tasks[0].time.strftime('%H:%M:%S')}开始工作"
                        context = f"下一次任务:{base_scheduler.tasks[0].plan if len(base_scheduler.tasks[0].plan) != 0 else '空任务' if base_scheduler.tasks[0].type == '' else base_scheduler.tasks[0].type}"
                        logger.info(context)
                        logger.info(subject)
                        base_scheduler.task_count += 1
                        logger.info(f"第{base_scheduler.task_count}次任务结束")
                        if remaining_time > 0:
                            if remaining_time > 300:
                                if config.conf.close_simulator_when_idle:
                                    restart_simulator(start=False)
                                elif config.conf.exit_game_when_idle:
                                    config.device.exit()
                            body = task_template.render(
                                tasks=[
                                    obj.format(timezone_offset)
                                    for obj in base_scheduler.tasks
                                ],
                                base_scheduler=base_scheduler,
                            )
                            send_message(body, subject)
                            config.idle = True
                            base_scheduler.sleep(remaining_time)
                            config.idle = False
                            base_scheduler.check_current_focus()

                elif remaining_time > 0:
                    now_time = datetime.now().time()
                    try:
                        min_time = datetime.strptime(
                            config.conf.maa_rg_sleep_min, "%H:%M"
                        ).time()
                        max_time = datetime.strptime(
                            config.conf.maa_rg_sleep_max, "%H:%M"
                        ).time()
                        if max_time < min_time:
                            rg_sleep = now_time > min_time or now_time < max_time
                        else:
                            rg_sleep = min_time < now_time < max_time
                    except ValueError:
                        rg_sleep = False

                    if not rg_sleep:
                        if config.conf.RA:
                            config.recog.update()
                            base_scheduler.back_to_index()
                            ra_solver = ReclamationAlgorithm()
                            ra_solver.run(base_scheduler.tasks[0].time - datetime.now())
                            remaining_time = (
                                base_scheduler.tasks[0].time - datetime.now()
                            ).total_seconds()
                        elif config.conf.SF:
                            config.recog.update()
                            base_scheduler.back_to_index()
                            sf_solver = SecretFront()
                            sf_solver.run(base_scheduler.tasks[0].time - datetime.now())
                            remaining_time = (
                                base_scheduler.tasks[0].time - datetime.now()
                            ).total_seconds()

                    subject = f"休息 {format_time(remaining_time)}，到{base_scheduler.tasks[0].time.strftime('%H:%M:%S')}开始工作"
                    context = f"下一次任务:{base_scheduler.tasks[0].plan}"
                    logger.info(context)
                    logger.info(subject)
                    base_scheduler.task_count += 1
                    logger.info(f"第{base_scheduler.task_count}次任务结束")
                    if remaining_time > 300:
                        if config.conf.close_simulator_when_idle:
                            restart_simulator(start=False)
                        elif config.conf.exit_game_when_idle:
                            config.device.exit()
                    body = task_template.render(
                        tasks=[
                            obj.format(timezone_offset) for obj in base_scheduler.tasks
                        ],
                        base_scheduler=base_scheduler,
                    )
                    send_message(body, subject)
                    config.idle = True
                    base_scheduler.sleep(remaining_time)
                    config.idle = False
                    base_scheduler.check_current_focus()

            base_scheduler.run()
            reconnect_tries = 0
        except MowerExit:
            return
        except (ConnectionError, ConnectionAbortedError, AttributeError) as e:
            logger.exception(e)
            reconnect_tries += 1
            if reconnect_tries < reconnect_max_tries:
                logger.warning("出现错误.尝试重启Mower")
                connected = False
                while not connected:
                    try:
                        base_scheduler = initialize([], base_scheduler)
                        break
                    except MowerExit:
                        raise
                    except Exception as e:
                        logger.exception(e)
                        restart_simulator()
                        config.device.client.check_server_alive()
                        Session().connect()
                        if config.conf.droidcast.enable:
                            config.device.start_droidcast()
                        if config.conf.touch_method == "scrcpy":
                            config.device.control.scrcpy = Scrcpy(config.device.client)
                        continue
                continue
            else:
                raise e
        except RuntimeError as e:
            logger.exception(f"程序出错-尝试重启模拟器->{e}")
            restart_simulator()
            config.device.client.check_server_alive()
            Session().connect()
            if config.conf.droidcast.enable:
                config.device.start_droidcast()
            if config.conf.touch_method == "scrcpy":
                config.device.control.scrcpy = Scrcpy(config.device.client)
        except Exception as e:
            logger.exception(f"程序出错--->{e}")
            config.recog.update()


def save_state(op_data, file="state.json"):
    tmp_dir = get_path("@app/tmp")
    if not tmp_dir.exists():
        tmp_dir.mkdir()
    state_file = tmp_dir / file
    with open(state_file, "w") as f:
        if op_data is not None:
            json.dump(vars(op_data), f, default=str)


def load_state(file="state.json"):
    state_file = get_path("@app/tmp") / file
    if not state_file.exists():
        return None
    with open(state_file, "r") as f:
        state = json.load(f)
    operators = {k: Expr(v).eval() for k, v in state["operators"].items()}
    for k, v in operators.items():
        if not v.time_stamp == "None":
            v.time_stamp = datetime.strptime(v.time_stamp, "%Y-%m-%d %H:%M:%S.%f")
        else:
            v.time_stamp = None
    logger.info("基建配置已加载！")
    return operators
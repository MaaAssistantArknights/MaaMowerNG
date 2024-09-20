import lzma
import pickle
from datetime import datetime, timedelta

import cv2
import numpy as np

from arknights_mower import __rootdir__
from arknights_mower.utils import config, rapidocr
from arknights_mower.utils.character_recognize import operator_room_select
from arknights_mower.utils.csleep import MowerExit
from arknights_mower.utils.image import cropimg, thres2
from arknights_mower.utils.log import logger

with lzma.open(f"{__rootdir__}/models/operator_room.model", "rb") as f:
    OP_ROOM = pickle.loads(f.read())

kernel = np.ones((12, 12), np.uint8)


class BaseMixin:
    def detect_arrange_order(self):
        name_list = ["工作状态", "技能", "心情", "信赖值"]
        x_list = (1196, 1320, 1445, 1572)
        y = 70
        mask = cv2.inRange(config.recog.hsv, (99, 200, 0), (100, 255, 255))
        for idx, x in enumerate(x_list):
            if np.count_nonzero(mask[y : y + 3, x : x + 5]):
                return (name_list[idx], True)
            if np.count_nonzero(mask[y + 10 : y + 13, x : x + 5]):
                return (name_list[idx], False)

    def switch_arrange_order(self, name, ascending=False):
        name_x = {"工作状态": 1197, "技能": 1322, "心情": 1447, "信赖值": 1575}
        if isinstance(name, int):
            name = list(name_x.keys())[name - 1]
        if isinstance(ascending, str):
            ascending = ascending == "true"
        name_y = 60
        self.tap((name_x[name], name_y), interval=0.5)
        while True:
            n, s = self.detect_arrange_order()
            if n == name and s == ascending:
                break
            self.tap((name_x[name], name_y), interval=0.5)

    def scan_agent(self, agent: list[str], error_count=0, max_agent_count=-1):
        try:
            # 识别干员
            while self.find("connecting"):
                logger.info("等待网络连接")
                self.sleep()
            # 返回的顺序是从左往右从上往下
            ret = operator_room_select(config.recog.img)
            # 提取识别出来的干员的名字
            select_name = []
            for name, scope in ret:
                if name in agent:
                    select_name.append(name)
                    # self.get_agent_detail((y[1][0]))
                    self.tap(scope, interval=0)
                    agent.remove(name)
                    # 如果是按照个数选择 Free
                    if max_agent_count != -1:
                        if len(select_name) >= max_agent_count:
                            return select_name, ret
            return select_name, ret
        except MowerExit:
            raise
        except Exception as e:
            logger.exception(e)
            error_count += 1
            if error_count < 3:
                self.sleep(3)
                return self.scan_agent(agent, error_count, max_agent_count)
            else:
                raise e

    def verify_agent(self, agent: list[str], error_count=0, max_agent_count=-1):
        try:
            # 识别干员
            while self.find("connecting"):
                logger.info("等待网络连接")
                self.sleep()
            ret = operator_room_select(config.recog.img)  # 返回的顺序是从左往右从上往下
            # 提取识别出来的干员的名字
            index = 0
            for name, scope in ret:
                if index >= len(agent):
                    return True
                if name != agent[index]:
                    return False
                index += 1
            return True
        except Exception as e:
            logger.exception(e)
            error_count += 1
            self.switch_arrange_order("技能")
            if error_count < 3:
                self.sleep(3)
                return self.verify_agent(agent, error_count, max_agent_count)
            else:
                raise e

    def swipe_left(self, right_swipe):
        if right_swipe > 3:
            self.detail_filter(控制中枢=True)
            self.detail_filter(控制中枢=False)
        else:
            swipe_time = 2 if right_swipe == 3 else right_swipe
            for i in range(swipe_time):
                self.swipe_noinertia((650, 540), (1900, 0))
        return 0

    def detail_filter(self, **kwargs):
        if kwargs:
            text = "，".join(
                f"{'打开' if value else '关闭'}{label}筛选"
                for label, value in kwargs.items()
            )
            text += "，关闭其余筛选"
            logger.info(text)
        else:
            logger.info("关闭所有筛选")

        labels = [
            "未进驻",
            "产出设施",
            "功能设施",
            "自定义设施",
            "控制中枢",
            "生产类后勤",
            "功能类后勤",
            "恢复类后勤",
        ]
        label_x = (560, 815, 1070, 1330)
        label_y = (540, 645)

        label_pos = []
        for y in label_y:
            for x in label_x:
                label_pos.append((x, y))

        label_pos_map = dict(zip(labels, label_pos))
        target_state = dict(zip(labels, [False] * len(labels)))
        target_state.update(kwargs)

        filter_pos = (config.recog.w * 0.95, config.recog.h * 0.05)
        self.tap(filter_pos)

        err_cnt = 0
        while not self.find("arrange_order_options_scene"):
            self.ctap(filter_pos)
            err_cnt += 1
            if err_cnt > 3:
                raise Exception("未进入筛选页面")

        for label, pos in label_pos_map.items():
            current_state = self.get_color(pos)[2] > 100
            if target_state[label] != current_state:
                self.tap(pos, interval=0.1)

        config.recog.update()
        confirm_pos = (config.recog.w * 0.8, config.recog.h * 0.8)
        self.tap(confirm_pos)

        err_cnt = 0
        while self.find("arrange_order_options_scene"):
            self.ctap(confirm_pos)
            err_cnt += 1
            if err_cnt > 3:
                raise Exception("筛选确认失败")

    def double_read_time(self, cord, upperLimit=None, use_digit_reader=False):
        config.recog.update()
        time_in_seconds = self.read_time(cord, upperLimit, use_digit_reader)
        if time_in_seconds is None:
            return datetime.now()
        execute_time = datetime.now() + timedelta(seconds=(time_in_seconds))
        return execute_time

    def read_accurate_mood(self, img):
        try:
            img = thres2(img, 200)
            return cv2.countNonZero(img) * 24 / 310
        except Exception as e:
            logger.exception(e)
            return 24

    def detect_product_complete(self):
        for product in ["gold", "exp", "lmd", "ori", "oru", "trust"]:
            if pos := self.find(
                f"infra_{product}_complete",
                scope=((1230, 0), (1920, 1080)),
                score=0.1,
            ):
                return pos

    def read_operator_in_room(self, img):
        img = thres2(img, 200)
        img = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, (0,))
        dilation = cv2.dilate(img, kernel, iterations=1)
        contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        rect = map(lambda c: cv2.boundingRect(c), contours)
        x, y, w, h = sorted(rect, key=lambda c: c[0])[0]
        img = img[y : y + h, x : x + w]
        tpl = np.zeros((46, 265), dtype=np.uint8)
        tpl[: img.shape[0], : img.shape[1]] = img
        tpl = cv2.copyMakeBorder(tpl, 2, 2, 2, 2, cv2.BORDER_CONSTANT, None, (0,))
        max_score = 0
        best_operator = None
        for operator, template in OP_ROOM.items():
            result = cv2.matchTemplate(tpl, template, cv2.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > max_score:
                max_score = max_val
                best_operator = operator
        return best_operator

    def read_screen(self, img, type="mood", limit=24, cord=None):
        if cord is not None:
            img = cropimg(img, cord)
        if type == "name":
            img = cropimg(img, ((169, 22), (513, 80)))
            return self.read_operator_in_room(img)
        try:
            ret = rapidocr.engine(img, use_det=False, use_cls=False, use_rec=True)[0]
            logger.debug(ret)
            if not ret or not ret[0][0]:
                raise Exception("识别失败")
            ret = ret[0][0]
            if "mood" in type:
                if (f"/{limit}") in ret:
                    ret = ret.replace(f"/{limit}", "")
                if len(ret) > 0:
                    if "." in ret:
                        ret = ret.replace(".", "")
                    return int(ret)
                else:
                    return -1
            elif "time" in type:
                if "." in ret:
                    ret = ret.replace(".", ":")
                return ret.strip()
            else:
                return ret
        except Exception as e:
            logger.exception(e)
            return limit + 1

    def read_time(self, cord, upperlimit, error_count=0, use_digit_reader=False):
        # 刷新图片
        config.recog.update()
        try:
            if use_digit_reader:
                time_str = self.digit_reader.get_time(config.recog.gray)
            else:
                time_str = self.read_screen(config.recog.img, type="time", cord=cord)
            h, m, s = str(time_str).split(":")
            if int(m) > 60 or int(s) > 60:
                raise Exception("读取错误")
            res = int(h) * 3600 + int(m) * 60 + int(s)
            if upperlimit is not None and res > upperlimit:
                raise Exception("超过读取上限")
            else:
                return res
        except Exception:
            if error_count > 3:
                logger.exception(f"读取失败{error_count}次超过上限")
                return None
            else:
                logger.exception("读取失败")
                return self.read_time(
                    cord, upperlimit, error_count + 1, use_digit_reader
                )
import cv2
from matplotlib import pyplot as plt
import numpy as np
from arknights_mower.utils import config
from arknights_mower.utils.log import logger
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.scene import Scene


class RIIC_Filter(SceneGraphSolver):
    def __init__(self) -> None:
        self.labels = [
            "未进驻",
            "产出设施",
            "功能设施",
            "自定义设施",
            "控制中枢",
            "生产类后勤",
            "功能类后勤",
            "恢复类后勤",
        ]

        self.orders = [
            "工作状态",
            "技能",
            "心情",
            "信赖值",
        ]
        label_x = (560, 815, 1070, 1330)
        label_y = (540, 645)

        label_pos = []
        for y in label_y:
            for x in label_x:
                label_pos.append((x, y))
        self.label_pos_map = dict(zip(self.labels, label_pos))

    def run(self, **kwargs):
        # 筛选标签 + True/False (开关标签) /None(切换状态)
        # 排序 + True/False 箭头朝(上/下)
        self.target_state = None
        self.order_label = None
        self.labels_chooed_done = False
        if kwargs:
            text = ""
            for self.label, value in kwargs.items():
                if self.label in self.orders and self.order_label is None:
                    self.order_label = self.label
                elif self.order_label is not None:
                    raise ValueError("排序参数仅有一个")
                text.join(f"{'打开' if value else '关闭'}{self.label}筛选")

            text += "，关闭其余筛选"
            logger.info(text)
        else:
            logger.info("关闭所有筛选")

        if self.target_state is None:
            self.target_state = dict(zip(self.labels, [False] * len(self.labels)))
            self.target_state.update(kwargs)

        logger.info(f"target_state :{self.target_state}")

        try:
            super().run()
        except ValueError as e:
            logger.error(e.__traceback__)

    def transition(self) -> bool:
        if (scene := self.scene()) == Scene.RIIC_OPERATOR_SELECT:
            if self.labels_chooed_done:
                if self.order_label in self.orders:
                    n, s = self.detect_arrange_order()
                    logger.info(f"detect_arrange_order {n}{s}")
                    logger.info(
                        f"order_label {self.order_label}{self.target_state[self.order_label]}"
                    )
                    if (
                        n != self.order_label
                        or s != self.target_state[self.order_label]
                    ):
                        self.switch_arrange_order(
                            self.order_label, self.target_state[self.order_label]
                        )
                        return
                return True
            else:
                self.tap_element("arrange_order_options")
        elif scene == Scene.INFRA_ARRANGE_ORDER:
            logger.debug(self.target_state)
            not_taped = True
            for label, pos in self.label_pos_map.items():
                current_state = self.get_color(pos)[2] > 100

                if self.target_state[label] is None:
                    self.target_state[label] = not current_state
                if self.target_state[label] != current_state:
                    not_taped = False
                    self.tap(pos, interval=0.1)
            if not_taped:
                confirm_pos = (config.recog.w * 0.8, config.recog.h * 0.8)
                self.tap(confirm_pos)
                self.labels_chooed_done = True
            else:
                return
        elif self.scene in self.waiting_scene:
            self.waiting_solver()
        else:
            return False

    def detect_arrange_order(self):
        x_list = (1196, 1320, 1445, 1572)
        y = 70
        hsv = cv2.cvtColor(config.recog.img, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, (99, 200, 0), (100, 255, 255))
        for idx, x in enumerate(x_list):
            if np.count_nonzero(mask[y : y + 3, x : x + 5]):
                return (self.orders[idx], True)
            if np.count_nonzero(mask[y + 10 : y + 13, x : x + 5]):
                return (self.orders[idx], False)

    def switch_arrange_order(self, name, ascending=False):
        name_x = {"工作状态": 1197, "技能": 1322, "心情": 1447, "信赖值": 1575}
        if isinstance(name, int):
            name = list(name_x.keys())[name - 1]
        if isinstance(ascending, str):
            ascending = ascending == "true"
        name_y = 60
        self.tap((name_x[name], name_y), interval=0.5)

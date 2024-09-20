import lzma
import pickle

import cv2
from matplotlib import pyplot as plt
import numpy as np
from arknights_mower.models import secret_front
from arknights_mower.solvers.filter import RIIC_Filter
from arknights_mower.utils import config
from arknights_mower.utils.character_recognize import (
    operator_room_select,
    match_portrait,
)
from arknights_mower.utils.image import cropimg
from arknights_mower.utils.log import logger
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower import __rootdir__
from arknights_mower.utils.scene import Scene
from arknights_mower.utils.vector import sa, va

# with lzma.open(f"{__rootdir__}/models/professior.pkl", "rb") as f:
#     pro_list = pickle.load(f)


class BaseChoose(SceneGraphSolver):
    def run(self, agent_list: list):
        self.agent_list = agent_list
        self.wait_choose = {}
        self.choosed = []
        self.cleard = False
        self.filter = RIIC_Filter()
        self.swipe_time = 0
        self.first_filter = True
        self.in_adjust = False
        self.tmp_data = {}

        try:
            super().run()
        except ValueError as e:
            logger.error(e.__traceback__)
            return False

    def riic_agent_choose(self):
        if len(list(set(self.choosed) & set(self.agent_list))) == len(self.agent_list):
            if self.check_agent_order():
                return True
            else:
                self.choosed.clear()
                self.first_filter = True
            return

        if self.wait_choose:
            logger.debug(f"待选名单{self.wait_choose}")
            iter = list(self.wait_choose.items())[0]
            # self.check_with_number(cropimg(config.recog.img,iter[1]))

            for i in self.get_agent_pos(only_choosed=True):
                if self.is_rectangle_contained(i, iter[1]):
                    del self.wait_choose[iter[0]]
                    self.choosed.append(iter[0])
                    logger.info(f"self.choosed:{self.choosed}")
                    return
            logger.debug(f"选择{iter}")
            self.tap(iter[1])
            return

        # 先清空 顺便调一下筛选
        if self.cleard is False:
            if self.first_filter:
                self.filter.run(未进驻=None)
                self.filter.run(技能=False)
                self.first_filter = False

            if self.get_agent_pos(only_choosed=True):
                self.tap_element("choose_agent/clear")
            else:
                self.cleard = True

            return

        initial_agents = operator_room_select(config.recog.img)

        agents = dict(initial_agents)

        if set(agents.keys()).issubset(self.tmp_data.keys()):
            self.swipe_time = self.swipe_time + 1
            if self.swipe_time > 3:
                raise ValueError("选择干员失败 滑动次数过多")

        self.tmp_data = agents
        logger.info(agents)

        intersection = list(set(agents.keys()) & set(self.agent_list))

        if intersection:
            for i in intersection:
                if i not in self.choosed:
                    self.wait_choose[i] = agents[i]
        if self.wait_choose:
            return
        else:
            # 加一个判断最右
            self.swipe_noinertia((1000, 540), (-1900, 0), interval=0.1)

    def check_agent_order(self):
        if self.in_adjust is False:
            choosed = self.get_agent_pos()
            if len(choosed) < len(self.agent_list):
                self.filter.run(未进驻=None)
                if len(self.get_agent_pos()) < len(self.agent_list):
                    logger.error("未选完全部干员")
                    return False
            elif len(choosed) == len(self.agent_list):
                for i in self.agent_list:
                    pos = self.agent_list.index(i) + 1
                    if choosed[i][0] != pos:
                        self.tmp_data = choosed
                        self.tap_element("choose_agent/clear")
                        self.in_adjust = True
                        return
                logger.debug(f"排序调整完成{choosed}")
                return True

        else:
            logger.info(self.tmp_data)
            for i in self.agent_list:
                rect = self.tmp_data[i][1]
                tap_pos = [
                    (rect[0][0] + rect[1][0]) / 2,
                    (rect[0][1] + rect[1][1]) / 2,
                ]
                self.tap(tap_pos)

            self.in_adjust = False
        return

    def check_with_number(self, img, height=61):
        _, im_w, _ = img.shape
        img = cropimg(img, ((0, 0), (im_w, 100)))
        kernel = np.ones((9, 9), np.uint8)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        img = cv2.inRange(img, (0, 0, 200), (225, 25, 255))

        img = cv2.erode(img, kernel)
        img = cv2.dilate(img, kernel)
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rect = [cv2.boundingRect(c) for c in contours]
        rect.sort(key=lambda c: c[0])
        value = 0
        for x, y, w, h in rect:
            digit = cropimg(img, ((x, y), (x + w, y + h)))
            digit = cv2.copyMakeBorder(
                digit, 10, 10, 10, 10, cv2.BORDER_CONSTANT, None, (0,)
            )

            if digit.shape[0] < 65 or digit.shape[1] < 40:
                continue
            score = []
            kernel = np.ones((2, 2), np.uint8)
            for i in range(10):
                im = secret_front[i]
                default_height = 25
                if height and height != default_height:
                    scale = default_height / height
                    digit_1 = cv2.resize(digit, None, None, scale, scale)

                im = cv2.dilate(im, kernel=kernel)
                result = cv2.matchTemplate(digit_1, im, cv2.TM_SQDIFF_NORMED)
                min_val, _, _, _ = cv2.minMaxLoc(result)
                score.append(min_val)
            value = value * 10 + score.index(min(score))
        return value

    def get_agent_pos(self, only_choosed=False):
        # only_choosed：仅需要判断被选中的位置，不需要具体信息
        pos_info = {}
        if only_choosed:
            pos_info = []
        seg = [[(550, 100), (1920, 534)], [(550, 530), (1920, 960)]]

        for i in seg:
            csc = cropimg(config.recog.img, i)
            csc_gray = cropimg(config.recog.gray, i)

            img = cv2.cvtColor(csc, cv2.COLOR_RGB2HSV)
            img = cv2.inRange(img, (90, 200, 180), (200, 255, 255))
            contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            rect = [cv2.boundingRect(c) for c in contours]
            rect.sort(key=lambda c: c[0])
            for x, y, w, h in rect:
                digit = cropimg(csc, ((x, y), (x + w, y + h)))

                if digit.size < 40000 or digit.size > 300000:
                    # 至少要露出半身才能识别到数字
                    # 基建选人防止多个框在一起的情况
                    continue

                if only_choosed:
                    pos_info.append(sa([(x, y), (x + w, y + h)], i[0]))
                else:
                    res = match_portrait(csc_gray, [((x, y), (x + w, y + h))])[0]
                    pos_info[res[0]] = [
                        self.check_with_number(digit),
                        sa([(x, y), (x + w, y + h)], i[0]),
                    ]
        return pos_info

    def is_rectangle_contained(self, rect1, rect2):
        # rect1和rect2都是(x, y, width, height)格式的四元组
        x11, y11 = rect1[0]
        x12, y12 = rect1[1]
        (
            x21,
            y21,
        ) = rect2[0]
        x22, y22 = rect2[1]
        a = (x22 + x21) / 2
        b = (y22 + y21) / 2
        # 如果rect2的左上角在rect1内，并且rect2完全在rect1的边界内，则认为rect2被rect1包含
        return x11 < (x22 + x21) / 2 < x12 and y11 < (y22 + y21) / 2 < y12

    def transition(self) -> bool:
        if (scene := self.scene()) == Scene.RIIC_OPERATOR_SELECT:
            return self.riic_agent_choose()
        elif scene == Scene.INFRA_ARRANGE_ORDER:
            logger.info(Scene.INFRA_ARRANGE_ORDER)
            self.scene_graph_navigation(Scene.RIIC_OPERATOR_SELECT)
        elif self.scene in self.waiting_scene:
            self.waiting_solver()
        else:
            return False

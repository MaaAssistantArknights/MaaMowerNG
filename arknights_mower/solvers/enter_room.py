from datetime import datetime, timedelta

import cv2

from arknights_mower.utils import config
from arknights_mower.utils import typealias as tp
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import cropimg, loadres
from arknights_mower.utils.log import logger
from arknights_mower.utils.recognize import Scene
from arknights_mower.utils.vector import sm, va

facility = {
    "central": (
        (-0.6551724137931034, -0.26436781609195403),
        (2.3524904214559386, 1.1340996168582376),
    ),
    "dormitory_1": (
        (-0.6615384615384616, 0.9692307692307693),
        (1.7538461538461538, 0.5115384615384616),
    ),
    "dormitory_2": (
        (-0.046153846153846156, 1.580769230769231),
        (1.7461538461538462, 0.5115384615384616),
    ),
    "dormitory_3": (
        (-0.6615384615384616, 2.1884615384615387),
        (1.7538461538461538, 0.5192307692307693),
    ),
    "dormitory_4": (
        (-0.046153846153846156, 2.7961538461538464),
        (1.7461538461538462, 0.5230769230769231),
    ),
    "factory": (
        (2.689655172413793, 0.9540229885057471),
        (1.1379310344827585, 0.5172413793103448),
    ),
    "meeting": (
        (2.0804597701149423, 0.3486590038314176),
        (1.747126436781609, 0.5172413793103448),
    ),
    "contact": (
        (2.689655172413793, 1.5632183908045976),
        (1.1379310344827585, 0.5172413793103448),
    ),
    "room_1_1": (
        (-4.626923076923077, 0.9692307692307693),
        (1.126923076923077, 0.5115384615384616),
    ),
    "room_1_2": (
        (-3.403846153846154, 0.9692307692307693),
        (1.123076923076923, 0.5115384615384616),
    ),
    "room_1_3": (
        (-2.184615384615385, 0.9692307692307693),
        (1.1307692307692307, 0.5115384615384616),
    ),
    "room_2_1": (
        (-5.2384615384615385, 1.580769230769231),
        (1.1346153846153846, 0.5115384615384616),
    ),
    "room_2_2": (
        (-4.015384615384615, 1.580769230769231),
        (1.1307692307692307, 0.5115384615384616),
    ),
    "room_2_3": (
        (-2.7923076923076926, 1.580769230769231),
        (1.126923076923077, 0.5115384615384616),
    ),
    "room_3_1": (
        (-4.6230769230769235, 2.1884615384615387),
        (1.123076923076923, 0.5192307692307693),
    ),
    "room_3_2": (
        (-3.4000000000000004, 2.1884615384615387),
        (1.123076923076923, 0.5192307692307693),
    ),
    "room_3_3": (
        (-2.180769230769231, 2.1884615384615387),
        (1.126923076923077, 0.5192307692307693),
    ),
    "train": (
        (2.689655172413793, 2.18007662835249),
        (1.1379310344827585, 0.5172413793103448),
    ),
}


class EnterRoomSolver(SceneGraphSolver):
    def run(self, room: str, detail: bool = True):
        """
        Args:
            room: 房间名
            detail: 打开进驻信息
        """
        logger.info(f"进入房间：{room}")
        self.room = room
        self.detail = detail
        self.wait_start()
        super().run()

    def timeout(self) -> bool:
        return datetime.now() > self.start_time + timedelta(seconds=3)

    def wait_start(self):
        self.start_time = datetime.now()

    def detect_room_number(self, img) -> int:
        score = []
        for i in range(1, 5):
            digit = loadres(f"room/{i}")
            result = cv2.matchTemplate(img, digit, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            score.append(max_val)
        return score.index(max(score)) + 1

    def detect_room(self) -> str:
        color_map = {
            "制造站": 25,
            "贸易站": 99,
            "发电站": 36,
            "训练室": 178,
            "加工站": 32,
        }
        img = cropimg(config.recog.img, ((568, 18), (957, 95)))
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        colored_room = None
        for room, color in color_map.items():
            mask = cv2.inRange(hsv, (color - 1, 0, 0), (color + 2, 255, 255))
            if cv2.countNonZero(mask) > 1000:
                colored_room = room
                break
        if colored_room in ["制造站", "贸易站", "发电站"]:
            digit_1 = cropimg(img, ((211, 24), (232, 54)))
            digit_2 = cropimg(img, ((253, 24), (274, 54)))
            digit_1 = self.detect_room_number(digit_1)
            digit_2 = self.detect_room_number(digit_2)
            logger.debug(f"{colored_room}B{digit_1}0{digit_2}")
            return f"room_{digit_1}_{digit_2}"
        elif colored_room == "训练室":
            logger.debug("训练室B305")
            return "train"
        elif colored_room == "加工站":
            logger.debug("加工站B105")
            return "factory"
        white_room = ["central", "dormitory", "meeting", "contact"]
        score = []
        for room in white_room:
            tpl = loadres(f"room/{room}")
            result = cv2.matchTemplate(img, tpl, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            score.append(max_val)
        room = white_room[score.index(max(score))]
        if room == "central":
            logger.debug("控制中枢")
        elif room == "dormitory":
            digit = cropimg(img, ((174, 24), (195, 54)))
            digit = self.detect_room_number(digit)
            if digit == 4:
                logger.debug("宿舍B401")
            else:
                logger.debug(f"宿舍B{digit}04")
            return f"dormitory_{digit}"
        elif room == "meeting":
            logger.debug("会客室1F02")
        else:
            logger.debug("办公室B205")
        return room

    @staticmethod
    def segment(central: tp.Scope) -> dict[str, tp.Rectangle]:
        top_left = central[0]
        width = central[1][0] - central[0][0]

        result = {}
        for name, (position, size) in facility.items():
            facility_top_left = va(top_left, sm(width, position))
            scope = facility_top_left, va(facility_top_left, sm(width, size))
            result[name] = (
                (round(max(scope[0][0], 0)), round(scope[0][1])),
                (round(min(scope[1][0], 1920)), round(scope[1][1])),
            )

        logger.debug(result)
        return result

    def transition(self) -> bool:
        if (scene := self.scene()) == Scene.INFRA_MAIN:
            if pos := self.find("control_central"):
                pos = self.segment(self.find("control_central"))[self.room]
                self.ctap(pos, 1, config.screenshot_avg / 1000)
                self.wait_start()
            else:
                config.recog.update()
        elif scene in [Scene.CTRLCENTER_ASSISTANT, Scene.INFRA_DETAILS]:
            if self.detect_room() == self.room:
                if not self.detail:
                    return True
                if self.find("room_detail"):
                    return True
                if pos := self.find("arrange_check_in"):
                    if self.find("infra_overview_top_right"):
                        self.ctap(pos, 1, config.screenshot_avg / 1000)
                    else:
                        config.recog.update()
                elif self.timeout():
                    self.scene_graph_step(Scene.INFRA_MAIN)
                else:
                    config.recog.update()
            else:
                if self.timeout():
                    self.scene_graph_step(Scene.INFRA_MAIN)
                else:
                    config.recog.update()
        else:
            self.scene_graph_step(Scene.INFRA_MAIN)

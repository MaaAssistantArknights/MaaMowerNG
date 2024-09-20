from datetime import datetime, timedelta

import cv2

from arknights_mower.utils import config
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import cropimg
from arknights_mower.utils.log import logger
from arknights_mower.utils.scene import Scene
from arknights_mower.utils.vector import sa

from .moon_festival import MoonFestival
from .utils import notify

activity_name = "良辰迎月"


class SignIn(SceneGraphSolver):
    def run(self):
        logger.info(f"Start: {activity_name}签到")
        self.in_progress = False
        self.start_time = datetime.now()
        self.success = False
        super().run()
        return self.success

    def transition(self) -> bool:
        if datetime.now() - self.start_time > timedelta(minutes=2):
            notify(f"{activity_name}签到超时", level="ERROR")
            return True
        elif (scene := self.scene()) == Scene.MATERIEL:
            self.sleep()
            notify(f"{activity_name}奖励领取")
            self.tap((960, 960))
        elif scene == Scene.INDEX:
            if pos := self.find("sign_in/entry"):
                self.tap(pos)
            else:
                notify(f"未找到{activity_name}签到入口")
                self.success = True
                return True
        elif scene == Scene.SIGN_IN_DAILY:
            top_left = 680, 500
            img = cropimg(config.recog.hsv, (top_left, (1800, 540)))
            img = cv2.inRange(img, (2, 180, 230), (15, 255, 255))
            contours, _ = cv2.findContours(
                img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            rect = [cv2.boundingRect(c) for c in contours]
            if len(rect) == 0:
                if not self.in_progress:
                    notify(f"{activity_name}签到奖励已领完")
                self.in_progress = False
                self.success = True
                return True
            rect.sort(key=lambda c: c[0])
            x, y, w, h = rect[0]
            scope = sa(((x, y), (x + w, y + h)), top_left)
            self.in_progress = True
            self.ctap(scope)
        elif scene == Scene.MOON_FESTIVAL:
            if MoonFestival().run():
                return
            return True
        else:
            self.scene_graph_step(Scene.INDEX)

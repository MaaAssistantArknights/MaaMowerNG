from datetime import datetime, timedelta

import cv2

from arknights_mower.utils import config
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import cropimg
from arknights_mower.utils.log import logger
from arknights_mower.utils.scene import Scene
from arknights_mower.utils.vector import sa

from .utils import notify

activity_name = "月饼烘焙小教程·三"


class MoonFestival(SceneGraphSolver):
    def run(self):
        logger.info(f"Start: {activity_name}")
        self.start_time = datetime.now()
        self.success = True
        super().run()
        return self.success

    def transition(self) -> bool:
        if datetime.now() - self.start_time > timedelta(minutes=1):
            notify(f"{activity_name}签到超时", level="ERROR")
            return True
        elif (scene := self.scene()) == Scene.MATERIEL:
            self.sleep()
            notify(f"{activity_name}奖励领取")
            self.tap((960, 960))
        elif scene in self.waiting_scene:
            self.waiting_solver()
        elif (scene := self.scene()) == Scene.MOON_FESTIVAL:
            if pos := self.find("sign_in/moon_festival/moon_cake"):
                self.tap(pos)
                return
            top_left = 530, 910
            img = cropimg(config.recog.hsv, (top_left, (1390, 1020)))
            img = cv2.inRange(img, (5, 180, 200), (15, 255, 255))
            contours, _ = cv2.findContours(
                img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            rect = [cv2.boundingRect(c) for c in contours]
            if len(rect) == 0:
                self.success = False
                self.back()
                return
            rect.sort(key=lambda c: c[0])
            x, y, w, h = rect[0]
            scope = sa(((x, y), (x + w, y + h)), top_left)
            self.ctap(scope)
        else:
            return True

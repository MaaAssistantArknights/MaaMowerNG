from datetime import datetime

import cv2

from arknights_mower.utils import config
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import loadres, saveimg
from arknights_mower.utils.log import logger
from arknights_mower.utils.matcher import (
    GOOD_DISTANCE_LIMIT,
    flann,
    keypoints_scale_invariant,
)
from arknights_mower.utils.scene import Scene
from arknights_mower.utils.vector import va, vs

from .utils import generate_name


class classproperty:
    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


class ActivityNavigation(SceneGraphSolver):
    _location = {
        "CV-1": (0, 0),
        "CV-2": (601, -175),
        "CV-3": (1181, -175),
        "CV-4": (1757, -175),
        "CV-5": (2344, -61),
        "CV-6": (2755, 55),
        "CV-7": (3208, -87),
        "CV-8": (3617, 2),
    }

    @classproperty
    def location(cls):
        if datetime.now() > datetime(2024, 9, 29, 4):
            return {}
        return cls._location

    def generate_names(self):
        names = {}
        for name in self._location.keys():
            names[name] = generate_name(name)
        self.names = names

    def run(self, name: str) -> None:
        logger.info("Start: 活动关卡导航")
        self.name = name
        self.generate_names()
        super().run()
        return True

    def transition(self) -> bool:
        if (scene := self.scene()) == Scene.TERMINAL_MAIN:
            img = loadres("navigation/activity/terminal.jpg", True)
            kp1, des1 = keypoints_scale_invariant(img)
            kp2, des2 = config.recog.matcher.kp, config.recog.matcher.des
            matches = flann.knnMatch(des1, des2, k=2)
            good = []
            for pair in matches:
                if (len_pair := len(pair)) == 2:
                    x, y = pair
                    if x.distance < GOOD_DISTANCE_LIMIT * y.distance:
                        good.append(x)
                elif len_pair == 1:
                    good.append(pair[0])
            good = sorted(good, key=lambda x: x.distance)
            debug_img = cv2.drawMatches(
                img,
                kp1,
                config.recog.gray,
                kp2,
                good[:10],
                None,
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
            )
            saveimg(debug_img, "navigation")
            self.tap(kp2[good[0].trainIdx].pt, interval=3)
        elif scene == Scene.ACTIVITY_MAIN:
            self.tap_element("navigation/activity/entry")
        elif scene == Scene.ACTIVITY_CHOOSE_LEVEL:
            name, val, loc = None, 1, None
            for n, img in self.names.items():
                result = cv2.matchTemplate(config.recog.gray, img, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if min_val < val:
                    val = min_val
                    loc = min_loc
                    name = n

            target = va(vs(loc, self.location[name]), self.location[self.name])
            if target[0] + 200 > 1920:
                self.swipe_noinertia((1400, 540), (-1000, 0))
            elif target[0] < 0:
                self.swipe_noinertia((400, 540), (1000, 0))
            else:
                self.tap(va(target, (60, 20)))
        elif scene == Scene.OPERATOR_BEFORE:
            return True
        else:
            self.scene_graph_step(Scene.TERMINAL_MAIN)

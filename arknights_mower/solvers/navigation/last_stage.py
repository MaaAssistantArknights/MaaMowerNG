import cv2

from arknights_mower.utils import config
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import cropimg, thres2
from arknights_mower.utils.log import logger
from arknights_mower.utils.scene import Scene

from .utils import last_letters


class LastStageNavigation(SceneGraphSolver):
    def run(self, name: str) -> None:
        self.name = name
        self.success = True
        if self.name != "":
            self.scene_graph_navigation(Scene.TERMINAL_MAIN)
        super().run()
        return self.success

    def last_stage(self) -> str:
        img = cropimg(config.recog.gray, ((1690, 845), (1870, 890)))
        dark_img = cv2.bitwise_not(img)
        dark_img = thres2(dark_img, 127)

        contours, _ = cv2.findContours(
            dark_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        rect = [cv2.boundingRect(c) for c in contours]
        rect.sort(key=lambda c: c[0])

        value = ""
        for x, y, w, h in rect:
            if h < 7:
                if w < 7:
                    continue
                value += "-"
                continue
            digit = cropimg(img, ((x, y), (x + w, y + h)))
            digit = cv2.copyMakeBorder(digit, 10, 10, 10, 10, cv2.BORDER_REPLICATE)
            score = {}
            for letter, letter_img in last_letters.items():
                try:
                    result = cv2.matchTemplate(digit, letter_img, cv2.TM_SQDIFF_NORMED)
                except Exception as e:
                    logger.exception(e)
                    return ""
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                score[letter] = min_val
            value += min(score, key=score.get)
        logger.debug(value)
        return value

    def transition(self) -> bool:
        if (scene := self.scene()) == Scene.TERMINAL_MAIN:
            if self.name in ["", self.last_stage()]:
                self.tap((1670, 880))
            else:
                self.success = False
                return True
        elif scene == Scene.OPERATOR_BEFORE:
            return True
        else:
            self.scene_graph_step(Scene.TERMINAL_MAIN)

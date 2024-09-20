import json
from datetime import datetime, timedelta

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from arknights_mower import __rootdir__
from arknights_mower.utils import config
from arknights_mower.utils import typealias as tp
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import cmatch, cropimg, loadres
from arknights_mower.utils.log import logger
from arknights_mower.utils.path import get_path
from arknights_mower.utils.recognize import Scene
from arknights_mower.utils.vector import va

font36 = ImageFont.truetype(f"{__rootdir__}/fonts/SourceHanSansCN-Medium.otf", size=36)
font30 = ImageFont.truetype(f"{__rootdir__}/fonts/SourceHanSansCN-Medium.otf", size=30)

xl = list(range(230, 1655, 473))
yl = [230, 573]
sl = []
for y in yl:
    for x in xl:
        tl = (x, y)
        sl.append((tl, va(tl, (10, 10))))


class SSSNaviSolver(SceneGraphSolver):
    def run(self) -> bool:
        logger.info("Start: 保全导航")
        self.start_time = datetime.now()
        self.success = False

        with get_path("@app/sss.json").open("r", encoding="utf-8") as f:
            copilot = json.load(f)
        self.type = self.generate_image(copilot["stage_name"], font36)
        self.ec = self.generate_image(copilot["buff"], font30)
        self.device: list[str] = copilot["equipment"]

        super().run()
        return self.success

    def generate_image(self, text: str, font) -> tp.GrayImage:
        img = Image.new(mode="L", size=(300, 70), color=(0,))
        draw = ImageDraw.Draw(img)
        draw.text((20, 0), text, fill=(255,), font=font)
        img = np.array(img, dtype=np.uint8)
        contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rect = [cv2.boundingRect(c) for c in contours]
        left = min(x for x, y, w, h in rect)
        right = max(x + w for x, y, w, h in rect)
        top = min(y for x, y, w, h in rect)
        bottom = max(y + h for x, y, w, h in rect)
        return cropimg(img, ((left - 2, top - 2), (right + 2, bottom + 2)))

    def get_device(self) -> list[str]:
        A = loadres("sss/A")
        result = []
        for scope in sl:
            img = cropimg(config.recog.img, scope)
            result.append("A" if cmatch(A, img, 60) else "B")
        logger.debug(result)
        return result

    def transition(self):
        if datetime.now() - self.start_time > timedelta(minutes=2):
            logger.error("保全导航超时")
            return True
        elif (scene := self.scene()) in [Scene.SSS_DEPLOY, Scene.SSS_REDEPLOY]:
            delta = (datetime.now() - self.start_time).total_seconds()
            logger.info(f"保全导航成功，用时{delta:.0f}秒")
            self.success = True
            return True
        elif scene == Scene.SSS_MAIN:
            pos = self.get_pos(config.recog.matcher.match(self.type, judge=False), 0)
            self.tap(va(pos, (-240, 0)))
        elif scene == Scene.SSS_START:
            self.tap_element("sss/start")
        elif scene == Scene.SSS_EC:
            self.tap(config.recog.matcher.match(self.ec, dpi_aware=True, judge=False))
            self.tap_element("sss/ec")
        elif scene == Scene.SSS_DEVICE:
            current = self.get_device()
            for i in range(8):
                if current[i] != self.device[i]:
                    self.tap(sl[i])
                    return
            self.tap_element("sss/device")
        elif scene == Scene.SSS_SQUAD:
            self.tap_element("sss/squad")

        else:
            self.scene_graph_step(Scene.SSS_MAIN)

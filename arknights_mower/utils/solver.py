import random
import time
from abc import abstractmethod
from datetime import datetime, timedelta
from typing import Literal, Optional, Tuple

import cv2
import numpy as np

from arknights_mower.data import scene_list
from arknights_mower.utils import config
from arknights_mower.utils import typealias as tp
from arknights_mower.utils.csleep import MowerExit, csleep
from arknights_mower.utils.device.adb_client.const import KeyCode
from arknights_mower.utils.device.adb_client.session import Session
from arknights_mower.utils.device.device import Device
from arknights_mower.utils.device.scrcpy import Scrcpy
from arknights_mower.utils.image import cropimg, thres2
from arknights_mower.utils.log import logger
from arknights_mower.utils.recognize import RecognizeError, Recognizer, Scene
from arknights_mower.utils.simulator import restart_simulator
from arknights_mower.utils.traceback import caller_info


class StrategyError(Exception):
    """Strategy Error"""

    pass


class BaseSolver:
    """Base class, provide basic operation"""

    tap_info = None, None
    waiting_scene = [
        Scene.CONNECTING,
        Scene.UNKNOWN,
        Scene.UNKNOWN_WITH_NAVBAR,
        Scene.LOADING,
        Scene.LOGIN_LOADING,
        Scene.LOGIN_MAIN_NOENTRY,
        Scene.OPERATOR_ONGOING,
    ]

    def __init__(self) -> None:
        if config.device is None:
            while True:
                try:
                    config.device = Device()
                    config.device.client.check_server_alive()
                    Session().connect()
                    if not config.device.check_device_screen():
                        raise MowerExit
                    if config.conf.droidcast.enable:
                        config.device.start_droidcast()
                    if config.conf.touch_method == "scrcpy":
                        config.device.control.scrcpy = Scrcpy(config.device.client)
                    break
                except MowerExit:
                    raise
                except Exception as e:
                    logger.exception(e)
                    restart_simulator()

        if config.recog is None:
            config.recog = Recognizer()

    def run(self) -> None:
        self.check_current_focus()
        retry_times = config.MAX_RETRYTIME
        result = None
        while retry_times > 0:
            try:
                result = self.transition()
                if result:
                    return result
            except MowerExit:
                raise
            except RecognizeError as e:
                logger.exception(f"识别出了点小差错 qwq: {e}")
                retry_times -= 1
                self.sleep(3)
                continue
            except Exception as e:
                logger.exception(e)
                raise e
            retry_times = config.MAX_RETRYTIME

    @abstractmethod
    def transition(self) -> bool:
        # the change from one state to another is called transition
        return True  # means task completed

    def get_color(self, pos: tp.Coordinate) -> tp.Pixel:
        """get the color of the pixel"""
        return config.recog.color(pos[0], pos[1])

    @staticmethod
    def get_pos(
        poly: tp.Location, x_rate: float = 0.5, y_rate: float = 0.5
    ) -> tp.Coordinate:
        """get the pos form tp.Location"""
        if poly is None:
            raise RecognizeError("poly is empty")
        elif len(poly) == 4:
            # tp.Rectangle
            x = (
                poly[0][0] * (1 - x_rate)
                + poly[1][0] * (1 - x_rate)
                + poly[2][0] * x_rate
                + poly[3][0] * x_rate
            ) / 2
            y = (
                poly[0][1] * (1 - y_rate)
                + poly[3][1] * (1 - y_rate)
                + poly[1][1] * y_rate
                + poly[2][1] * y_rate
            ) / 2
        elif len(poly) == 2 and isinstance(poly[0], (list, tuple)):
            # tp.Scope
            x = poly[0][0] * (1 - x_rate) + poly[1][0] * x_rate
            y = poly[0][1] * (1 - y_rate) + poly[1][1] * y_rate
        else:
            # tp.Coordinate
            x, y = poly
        return (int(x), int(y))

    def sleep(self, interval: float = 1) -> None:
        """sleeping for a interval"""
        csleep(interval)
        config.recog.update()

    def input(self, referent: str, input_area: tp.Scope, text: str = None) -> None:
        """input text"""
        logger.debug(f"{referent=} {input_area=}")
        config.device.tap(self.get_pos(input_area))
        time.sleep(0.5)
        if text is None:
            text = input(referent).strip()
        config.device.send_text(str(text))
        config.device.tap((0, 0))

    def find(
        self,
        res: tp.Res,
        draw: bool = False,
        scope: tp.Scope = None,
        thres: int = None,
        judge: bool = True,
        strict: bool = False,
        score=0.0,
    ) -> tp.Scope:
        return config.recog.find(res, draw, scope, thres, judge, strict, score)

    def tap(
        self,
        poly: tp.Location,
        x_rate: float = 0.5,
        y_rate: float = 0.5,
        interval: float = 1,
    ) -> None:
        """tap"""
        if config.stop_mower.is_set():
            raise MowerExit
        self.tap_info = None, None
        pos = self.get_pos(poly, x_rate, y_rate)
        config.device.tap(pos)
        if interval > 0:
            self.sleep(interval)

    def ctap(
        self, pos: tp.Location, max_seconds: float = 10, interval: float = 1
    ) -> bool:
        """同一处代码多次调用ctap，在max_seconds时长内最多点击一次
        Args:
            pos: 点击位置
            max_seconds: 等待网络连接建议设10，等待动画建议设5或3
            interval: 点击后sleep的时长
        Returns:
            本次点击是否成功
        """
        id = caller_info()
        now = datetime.now()
        lid, ltime = self.tap_info
        if lid != id or (lid == id and now - ltime > timedelta(seconds=max_seconds)):
            logger.debug(f"tap {id}")
            self.tap(pos, interval=interval)
            self.tap_info = id, now
            return True
        else:
            self.sleep(interval)
            logger.debug(f"skip {id}")
            return False

    def check_current_focus(self):
        config.recog.check_current_focus()

    def restart_game(self):
        "重启游戏"
        config.device.exit()
        config.device.launch()
        config.recog.update()

    def tap_element(
        self,
        element_name: tp.Res,
        x_rate: float = 0.5,
        y_rate: float = 0.5,
        interval: float = 1,
        score: float = 0.0,
        draw: bool = False,
        scope: tp.Scope = None,
        judge: bool = True,
        detected: bool = False,
        thres: Optional[int] = None,
    ) -> bool:
        """tap element"""
        element = self.find(
            element_name, draw, scope, judge=judge, score=score, thres=thres
        )
        if detected and element is None:
            return False
        self.tap(element, x_rate, y_rate, interval)
        return True

    def tap_index_element(
        self,
        name: Literal[
            "friend",
            "infrastructure",
            "mission",
            "recruit",
            "shop",
            "terminal",
            "warehouse",
            "headhunting",
            "mail",
        ],
    ):
        pos = {
            "friend": (544, 862),  # 好友
            "infrastructure": (1545, 948),  # 基建
            "mission": (1201, 904),  # 任务
            "recruit": (1507, 774),  # 公开招募
            "shop": (1251, 727),  # 采购中心
            "terminal": (1458, 297),  # 终端
            "warehouse": (1788, 973),  # 仓库
            "headhunting": (1749, 783),  # 干员寻访
            "mail": (292, 62),  # 邮件
        }
        self.ctap(pos[name])

    def tap_nav_element(
        self,
        name: Literal[
            "index",
            "terminal",
            "infrastructure",
            "recruit",
            "headhunting",
            "shop",
            "mission",
            "friend",
        ],
    ):
        pos = {
            "index": (140, 365),  # 首页
            "terminal": (793, 163),  # 终端
            "infrastructure": (1030, 163),  # 基建
            "recruit": (1435, 365),  # 公开招募
            "headhunting": (1623, 364),  # 干员寻访
            "shop": (1804, 362),  # 采购中心
            "mission": (1631, 53),  # 任务
            "friend": (1801, 53),  # 好友
        }
        self.ctap(pos[name])

    def tap_terminal_button(
        self,
        name: Literal[
            "main",
            "main_theme",
            "intermezzi",
            "biography",
            "collection",
            "regular",
            "longterm",
            "contract",
        ],
    ):
        y = 1005
        pos = {
            "main": (115, y),  # 首页
            "main_theme": (356, y),  # 主题曲
            "intermezzi": (596, y),  # 插曲
            "biography": (836, y),  # 别传
            "collection": (1077, y),  # 资源收集
            "regular": (1317, y),  # 常态事务
            "longterm": (1556, y),  # 长期探索
            "contract": (1796, y),  # 危机合约
        }
        self.ctap(pos[name])

    def template_match(
        self,
        res: str,
        scope: Optional[tp.Scope] = None,
        method: int = cv2.TM_CCOEFF_NORMED,
    ) -> Tuple[float, tp.Scope]:
        return config.recog.template_match(res, scope, method)

    def swipe(
        self,
        start: tp.Coordinate,
        movement: tp.Coordinate,
        duration: int = 100,
        interval: float = 1,
    ) -> None:
        """swipe"""
        if config.stop_mower.is_set():
            raise MowerExit
        end = (start[0] + movement[0], start[1] + movement[1])
        config.device.swipe(start, end, duration=duration)
        if interval > 0:
            self.sleep(interval)

    def swipe_only(
        self,
        start: tp.Coordinate,
        movement: tp.Coordinate,
        duration: int = 100,
        interval: float = 1,
    ) -> None:
        """swipe only, no rebuild and recapture"""
        if config.stop_mower.is_set():
            raise MowerExit
        end = (start[0] + movement[0], start[1] + movement[1])
        config.device.swipe(start, end, duration=duration)
        if interval > 0:
            csleep(interval)

    # def swipe_seq(self, points: list[tp.Coordinate], duration: int = 100, interval: float = 1, rebuild: bool = True) -> None:
    #     """ swipe with point sequence """
    #     config.device.swipe(points, duration=duration)
    #     if interval > 0:
    #         self.sleep(interval, rebuild)

    # def swipe_move(self, start: tp.Coordinate, movements: list[tp.Coordinate], duration: int = 100, interval: float = 1, rebuild: bool = True) -> None:
    #     """ swipe with start and movement sequence """
    #     points = [start]
    #     for move in movements:
    #         points.append((points[-1][0] + move[0], points[-1][1] + move[1]))
    #     config.device.swipe(points, duration=duration)
    #     if interval > 0:
    #         self.sleep(interval, rebuild)

    def swipe_noinertia(
        self,
        start: tp.Coordinate,
        movement: tp.Coordinate,
        duration: int = 20,
        interval: float = 0.2,
    ) -> None:
        """swipe with no inertia (movement should be vertical)"""
        if config.stop_mower.is_set():
            raise MowerExit
        points = [start]
        if movement[0] == 0:
            dis = abs(movement[1])
            points.append((start[0] + 100, start[1]))
            points.append((start[0] + 100, start[1] + movement[1]))
            points.append((start[0], start[1] + movement[1]))
        else:
            dis = abs(movement[0])
            points.append((start[0], start[1] + 100))
            points.append((start[0] + movement[0], start[1] + 100))
            points.append((start[0] + movement[0], start[1]))
        config.device.swipe_ext(points, durations=[200, dis * duration // 100, 200])
        if interval > 0:
            self.sleep(interval)

    def back(self, interval: float = 1) -> None:
        """send back keyevent"""
        self.tap_info = None, None
        config.device.send_keyevent(KeyCode.KEYCODE_BACK)
        self.sleep(interval)

    def cback(self, max_seconds: float = 10, interval: float = 1) -> bool:
        """同一处代码多次调用cback，在max_seconds时长内最多返回一次
        Args:
            max_seconds: 等待网络连接建议设10，等待动画建议设5或3
            interval: 点击后sleep的时长
        Returns:
            本次点击是否成功
        """
        id = caller_info()
        now = datetime.now()
        lid, ltime = self.tap_info
        if lid != id or (lid == id and now - ltime > timedelta(seconds=max_seconds)):
            logger.debug(f"tap {id}")
            self.back(interval=interval)
            self.tap_info = id, now
            return True
        else:
            self.sleep(interval)
            logger.debug(f"skip {id}")
            return False

    def scene(self) -> int:
        """get the current scene in the game"""
        return config.recog.get_scene()

    def ra_scene(self) -> int:
        """
        生息演算场景识别
        """
        return config.recog.get_ra_scene()

    def sf_scene(self) -> int:
        """
        隐秘战线场景识别
        """
        return config.recog.get_sf_scene()

    def train_scene(self) -> int:
        """
        训练室景识别
        """
        return config.recog.get_train_scene()

    def solve_captcha(self, refresh=False):
        th = thres2(config.recog.gray, 254)
        pos = np.nonzero(th)
        offset_x = pos[1].min()
        offset_y = pos[0].min()
        img_scope = ((offset_x, offset_y), (pos[1].max(), pos[0].max()))
        img = cropimg(config.recog.img, img_scope)
        h = img.shape[0]

        def _t(ratio):
            return int(h * ratio)

        def _p(ratio_x, ratio_y):
            return _t(ratio_x), _t(ratio_y)

        if refresh:
            logger.info("刷新验证码")
            self.tap((offset_x + _t(0.189), offset_y + _t(0.916)), interval=3)
            img = cropimg(config.recog.img, img_scope)

        left_part = cropimg(img, (_p(0.032, 0.032), _p(0.202, 0.591)))
        hsv = cv2.cvtColor(left_part, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, (25, 0, 0), (35, 255, 255))

        tpl_width = _t(0.148)
        tpl_height = _t(0.135)
        tpl_border = _t(0.0056)
        tpl_padding = _t(0.018)
        tpl = np.zeros((tpl_height, tpl_width), np.uint8)
        tpl[:] = (255,)
        tpl[
            tpl_border : tpl_height - tpl_border,
            tpl_border : tpl_width - tpl_border,
        ] = (0,)

        result = cv2.matchTemplate(mask, tpl, cv2.TM_SQDIFF, None, tpl)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        x, y = min_loc

        source_p = (
            (x + tpl_padding, y + tpl_padding),
            (x + tpl_width - tpl_padding, y + tpl_height - tpl_padding),
        )
        source = cropimg(left_part, source_p)
        mask = cropimg(mask, source_p)
        right_part = cropimg(
            img,
            (
                (_t(0.201), _t(0.032) + source_p[0][1]),
                (_t(0.94), _t(0.032) + source_p[1][1]),
            ),
        )

        for _y in range(source.shape[0]):
            for _x in range(source.shape[1]):
                for _c in range(source.shape[2]):
                    source[_y, _x, _c] = np.clip(source[_y, _x, _c] * 0.7 - 23, 0, 255)

        mask = cv2.bitwise_not(mask)
        result = cv2.matchTemplate(right_part, source, cv2.TM_SQDIFF_NORMED, None, mask)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        x = _t(0.201) + min_loc[0] - _t(0.032) - x - tpl_padding + _t(0.128)
        x += random.choice([-4, -3, -2, 2, 3, 4])

        def _rb(R, r):
            return random.random() * _t(R) + _t(r)

        btn_x = _rb(0.1, 0.01)
        start = offset_x + btn_x + _t(0.128), offset_y + _rb(0.1, 0.01) + _t(0.711)
        end = offset_x + btn_x + x, offset_y + _rb(0.1, 0.01) + _t(0.711)
        p1 = end[0] + _rb(0.1, 0.02), end[1] + _rb(0.05, 0.02)
        p2 = end[0] + _rb(0.1, 0.02), end[1] + _rb(0.05, 0.02)

        logger.info("滑动验证码")
        config.device.swipe_ext(
            (start, p1, p2, end, end),
            durations=[
                random.randint(400, 600),
                random.randint(200, 300),
                random.randint(200, 300),
                random.randint(200, 300),
            ],
        )

    def waiting_solver(self):
        """需要等待的页面解决方法。UNKNOWN_WITH_NAVBAR超时直接返回False,其他超时重启返回False"""
        scene = self.scene()
        start_time = datetime.now()
        sleep_time, wait_time = getattr(
            config.conf.waiting_scene_v2, scene_list[str(scene)]["label"]
        )
        stop_time = start_time + timedelta(seconds=wait_time)
        while datetime.now() < stop_time:
            self.sleep(sleep_time / 1000)
            if self.scene() != scene:
                return True
        if scene == Scene.UNKNOWN_WITH_NAVBAR:
            logger.debug("有导航栏的未知场景超时")
            return False
        else:
            logger.warning("相同场景等待超时")
            config.device.exit()
            csleep(3)
            self.check_current_focus()
            return False

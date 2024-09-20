from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 其它场景


@edge(Scene.UNDEFINED, Scene.INDEX)
def get_scene(solver: BaseSolver):
    solver.scene()


@edge(Scene.LOGIN_START, Scene.LOGIN_QUICKLY)
def login_start(solver: BaseSolver):
    solver.tap((665, 741))


@edge(Scene.CONFIRM, Scene.LOGIN_START)
def confirm(solver: BaseSolver):
    solver.tap_element("confirm")


@edge(Scene.NOTICE, Scene.INDEX)
def close_notice(solver: BaseSolver):
    solver.tap_element("notice")


@edge(Scene.NETWORK_CHECK, Scene.LOGIN_START)
def network_check_cancel(solver: BaseSolver):
    solver.tap_element("confirm")


@edge(Scene.MOON_FESTIVAL, Scene.SIGN_IN_DAILY)
def moon_festival(solver: BaseSolver):
    solver.back()

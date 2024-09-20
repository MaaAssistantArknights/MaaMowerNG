from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 公招


@edge(Scene.RECRUIT_AGENT, Scene.RECRUIT_MAIN)
def recruit_result(solver: BaseSolver):
    solver.tap((960, 540))


@edge(Scene.REFRESH_TAGS, Scene.RECRUIT_TAGS)
def refresh_cancel(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=0)


@edge(Scene.RECRUIT_TAGS, Scene.RECRUIT_MAIN)
def recruit_back(solver: BaseSolver):
    solver.back()


@edge(Scene.SKIP, Scene.RECRUIT_AGENT)
def skip(solver: BaseSolver):
    solver.tap_element("skip")

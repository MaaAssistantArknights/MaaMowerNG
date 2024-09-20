from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 保全


@edge(Scene.TERMINAL_REGULAR, Scene.SSS_MAIN)
def enter_sss(solver: BaseSolver):
    solver.tap((1548, 870))


@edge(Scene.SSS_MAIN, Scene.TERMINAL_REGULAR)
@edge(Scene.SSS_START, Scene.SSS_MAIN)
@edge(Scene.SSS_DEPLOY, Scene.SSS_MAIN)
@edge(Scene.SSS_EC, Scene.SSS_EXIT_CONFIRM)
@edge(Scene.SSS_DEVICE, Scene.SSS_EXIT_CONFIRM)
@edge(Scene.SSS_SQUAD, Scene.SSS_EXIT_CONFIRM)
@edge(Scene.SSS_DEPLOY, Scene.SSS_MAIN)
@edge(Scene.SSS_REDEPLOY, Scene.SSS_MAIN)
@edge(Scene.SSS_TERMINATED, Scene.SSS_START)
def sss_back(solver: BaseSolver):
    solver.back()


@edge(Scene.SSS_EXIT_CONFIRM, Scene.SSS_TERMINATED)
def sss_exit(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=1)

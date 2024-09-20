from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 任务


@edge(Scene.MISSION_DAILY, Scene.MISSION_WEEKLY)
@edge(Scene.MISSION_TRAINEE, Scene.MISSION_WEEKLY)
def mission_to_weekly(solver: BaseSolver):
    solver.tap_element("mission_weekly")


@edge(Scene.MISSION_TRAINEE, Scene.MISSION_DAILY)
def mission_trainee_to_daily(solver: BaseSolver):
    solver.tap_element("mission_daily")

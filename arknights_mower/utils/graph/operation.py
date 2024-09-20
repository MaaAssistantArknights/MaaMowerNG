from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 作战


@edge(Scene.OPERATOR_RECOVER_POTION, Scene.OPERATOR_BEFORE)
@edge(Scene.OPERATOR_RECOVER_ORIGINITE, Scene.OPERATOR_BEFORE)
@edge(Scene.OPERATOR_BEFORE, Scene.OPERATOR_CHOOSE_LEVEL)
@edge(Scene.OPERATOR_CHOOSE_LEVEL, Scene.TERMINAL_MAIN_THEME)
@edge(Scene.OPERATOR_CHOOSE_LEVEL, Scene.TERMINAL_BIOGRAPHY)
@edge(Scene.OPERATOR_CHOOSE_LEVEL, Scene.TERMINAL_COLLECTION)
@edge(Scene.ACTIVITY_MAIN, Scene.TERMINAL_MAIN)
@edge(Scene.ACTIVITY_CHOOSE_LEVEL, Scene.ACTIVITY_MAIN)
@edge(Scene.OPERATOR_SUPPORT, Scene.OPERATOR_SELECT)
@edge(Scene.OPERATOR_STRANGER_SUPPORT, Scene.OPERATOR_SUPPORT)
@edge(Scene.OPERATOR_ELIMINATE_AGENCY, Scene.OPERATOR_ELIMINATE)
def operation_back(solver: BaseSolver):
    solver.back()


@edge(Scene.OPERATOR_GIVEUP, Scene.OPERATOR_FAILED)
def operation_give_up(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=1)


@edge(Scene.OPERATOR_FINISH, Scene.OPERATOR_BEFORE)
@edge(Scene.OPERATOR_FAILED, Scene.OPERATOR_BEFORE)
def operation_finish(solver: BaseSolver):
    solver.tap((310, 330))


@edge(Scene.UPGRADE, Scene.OPERATOR_FINISH)
def upgrade(solver: BaseSolver):
    solver.tap((960, 540))

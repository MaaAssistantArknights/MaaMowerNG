from arknights_mower.utils import config
from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 基建


@edge(Scene.INFRA_TODOLIST, Scene.INFRA_MAIN)
def todo_complete(solver: BaseSolver):
    solver.tap((1840, 140))


@edge(Scene.INFRA_CONFIDENTIAL, Scene.INFRA_MAIN)
@edge(Scene.INFRA_ARRANGE, Scene.INFRA_MAIN)
@edge(Scene.INFRA_DETAILS, Scene.INFRA_MAIN)
@edge(Scene.CTRLCENTER_ASSISTANT, Scene.INFRA_MAIN)
@edge(Scene.RIIC_OPERATOR_SELECT, Scene.INFRA_DETAILS)
@edge(Scene.CLUE_DAILY, Scene.INFRA_CONFIDENTIAL)
@edge(Scene.CLUE_RECEIVE, Scene.INFRA_CONFIDENTIAL)
@edge(Scene.CLUE_GIVE_AWAY, Scene.INFRA_CONFIDENTIAL)
@edge(Scene.CLUE_SUMMARY, Scene.INFRA_CONFIDENTIAL)
@edge(Scene.CLUE_PLACE, Scene.INFRA_CONFIDENTIAL)
@edge(Scene.ORDER_LIST, Scene.INFRA_DETAILS)
@edge(Scene.FACTORY_ROOMS, Scene.INFRA_DETAILS)
@edge(Scene.DRONE_ACCELERATE, Scene.ORDER_LIST)
def infra_back(solver: BaseSolver):
    solver.cback(1, config.screenshot_avg / 1000)


@edge(Scene.INFRA_ARRANGE_CONFIRM, Scene.INFRA_DETAILS)
def infra_arrange_confirm(solver: BaseSolver):
    solver.tap((1452, 1029))


@edge(Scene.INFRA_ARRANGE_ORDER, Scene.INFRA_DETAILS)
def infra_arrange_order(solver: BaseSolver):
    solver.tap_element("arrange_blue_yes", x_rate=0.66)


@edge(Scene.RIIC_REPORT, Scene.CTRLCENTER_ASSISTANT)
def riic_back(solver: BaseSolver):
    solver.tap((30, 55))


@edge(Scene.CTRLCENTER_ASSISTANT, Scene.RIIC_REPORT)
def riic(solver: BaseSolver):
    solver.tap_element("control_central_assistants")


@edge(Scene.INFRA_MAIN, Scene.CTRLCENTER_ASSISTANT)
def control_central(solver: BaseSolver):
    solver.tap_element("control_central")


@edge(Scene.SANITY_CHARGE, Scene.INFRA_MAIN)
def sanity_charge(solver: BaseSolver):
    solver.tap((1200, 15))


@edge(Scene.SANITY_CHARGE_DIALOG, Scene.SANITY_CHARGE)
def sanity_charge_dialog(solver: BaseSolver):
    solver.tap((480, 925))

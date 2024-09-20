from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 商店


@edge(Scene.SHOP_OTHERS, Scene.SHOP_CREDIT)
def shop_to_credit(solver: BaseSolver):
    solver.tap_element("shop_credit_2")


@edge(Scene.SHOP_CREDIT_CONFIRM, Scene.SHOP_CREDIT)
def shop_confirm(solver: BaseSolver):
    solver.back()


@edge(Scene.SHOP_UNLOCK_SCHEDULE, Scene.SHOP_CREDIT)
def schedule_to_shop(solver: BaseSolver):
    solver.back()

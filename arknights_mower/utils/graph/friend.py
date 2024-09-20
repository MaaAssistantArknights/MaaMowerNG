from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 好友


@edge(Scene.BUSINESS_CARD, Scene.FRIEND_LIST)
def friend_list(solver: BaseSolver):
    solver.tap((194, 333))


@edge(Scene.FRIEND_LIST, Scene.BUSINESS_CARD)
def business_card(solver: BaseSolver):
    solver.tap((188, 198))


@edge(Scene.FRIEND_VISITING, Scene.BACK_TO_FRIEND_LIST)
def friend_visiting_back(solver: BaseSolver):
    solver.back()


@edge(Scene.BACK_TO_FRIEND_LIST, Scene.BUSINESS_CARD)
def back_to_friend_confirm(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=1)

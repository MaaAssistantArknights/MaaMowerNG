from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 导航栏


@edge(Scene.INFRA_MAIN, Scene.NAVIGATION_BAR)
@edge(Scene.RECRUIT_MAIN, Scene.NAVIGATION_BAR)
@edge(Scene.RECRUIT_TAGS, Scene.NAVIGATION_BAR)
@edge(Scene.MISSION_DAILY, Scene.NAVIGATION_BAR)
@edge(Scene.MISSION_WEEKLY, Scene.NAVIGATION_BAR)
@edge(Scene.MISSION_TRAINEE, Scene.NAVIGATION_BAR)
@edge(Scene.BUSINESS_CARD, Scene.NAVIGATION_BAR)
@edge(Scene.FRIEND_LIST, Scene.NAVIGATION_BAR)
@edge(Scene.SHOP_OTHERS, Scene.NAVIGATION_BAR)
@edge(Scene.SHOP_CREDIT, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_MAIN, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_MAIN_THEME, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_EPISODE, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_BIOGRAPHY, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_COLLECTION, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_REGULAR, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_LONGTERM, Scene.NAVIGATION_BAR)
@edge(Scene.TERMINAL_PERIODIC, Scene.NAVIGATION_BAR)
@edge(Scene.OPERATOR_CHOOSE_LEVEL, Scene.NAVIGATION_BAR)
@edge(Scene.OPERATOR_BEFORE, Scene.NAVIGATION_BAR)
@edge(Scene.OPERATOR_SELECT, Scene.NAVIGATION_BAR)
@edge(Scene.OPERATOR_SUPPORT, Scene.NAVIGATION_BAR)
@edge(Scene.INFRA_TODOLIST, Scene.NAVIGATION_BAR)
@edge(Scene.INFRA_CONFIDENTIAL, Scene.NAVIGATION_BAR)
@edge(Scene.INFRA_ARRANGE, Scene.NAVIGATION_BAR)
@edge(Scene.INFRA_DETAILS, Scene.NAVIGATION_BAR)
@edge(Scene.CTRLCENTER_ASSISTANT, Scene.NAVIGATION_BAR)
@edge(Scene.CLUE_DAILY, Scene.NAVIGATION_BAR)
@edge(Scene.CLUE_RECEIVE, Scene.NAVIGATION_BAR)
@edge(Scene.CLUE_PLACE, Scene.NAVIGATION_BAR)
@edge(Scene.ORDER_LIST, Scene.NAVIGATION_BAR)
@edge(Scene.FACTORY_ROOMS, Scene.NAVIGATION_BAR)
@edge(Scene.OPERATOR_ELIMINATE, Scene.NAVIGATION_BAR)
@edge(Scene.DEPOT, Scene.NAVIGATION_BAR)
@edge(Scene.FRIEND_VISITING, Scene.NAVIGATION_BAR)
@edge(Scene.HEADHUNTING, Scene.NAVIGATION_BAR)
@edge(Scene.UNKNOWN_WITH_NAVBAR, Scene.NAVIGATION_BAR)
@edge(Scene.SSS_MAIN, Scene.NAVIGATION_BAR)
@edge(Scene.SSS_START, Scene.NAVIGATION_BAR)
@edge(Scene.ACTIVITY_MAIN, Scene.NAVIGATION_BAR)
@edge(Scene.ACTIVITY_CHOOSE_LEVEL, Scene.NAVIGATION_BAR)
def index_nav(solver: BaseSolver):
    solver.tap_element("nav_button")


# 不加从导航栏到基建首页的边，防止在基建内循环


@edge(Scene.NAVIGATION_BAR, Scene.MISSION_DAILY)
def nav_mission(solver: BaseSolver):
    solver.tap_nav_element("mission")


@edge(Scene.NAVIGATION_BAR, Scene.INDEX)
def nav_index(solver: BaseSolver):
    solver.tap_nav_element("index")


@edge(Scene.NAVIGATION_BAR, Scene.TERMINAL_MAIN)
def nav_terminal(solver: BaseSolver):
    solver.tap_nav_element("terminal")


@edge(Scene.NAVIGATION_BAR, Scene.RECRUIT_MAIN)
def nav_recruit(solver: BaseSolver):
    solver.tap_nav_element("recruit")


@edge(Scene.NAVIGATION_BAR, Scene.SHOP_OTHERS)
def nav_shop(solver: BaseSolver):
    solver.tap_nav_element("shop")


@edge(Scene.NAVIGATION_BAR, Scene.HEADHUNTING)
def nav_headhunting(solver: BaseSolver):
    solver.tap_nav_element("headhunting")


@edge(Scene.NAVIGATION_BAR, Scene.BUSINESS_CARD)
def nav_friend(solver: BaseSolver):
    solver.tap_nav_element("friend")

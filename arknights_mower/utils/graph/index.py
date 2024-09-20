from arknights_mower.utils import config
from arknights_mower.utils.scene import Scene
from arknights_mower.utils.solver import BaseSolver

from .utils import edge

# 首页


@edge(Scene.INFRA_MAIN, Scene.INDEX)
@edge(Scene.MISSION_DAILY, Scene.INDEX)
@edge(Scene.MISSION_WEEKLY, Scene.INDEX)
@edge(Scene.MISSION_TRAINEE, Scene.INDEX)
@edge(Scene.BUSINESS_CARD, Scene.INDEX)
@edge(Scene.FRIEND_LIST, Scene.INDEX)
@edge(Scene.RECRUIT_MAIN, Scene.INDEX)
@edge(Scene.SHOP_OTHERS, Scene.INDEX)
@edge(Scene.SHOP_CREDIT, Scene.INDEX)
@edge(Scene.TERMINAL_MAIN, Scene.INDEX)
@edge(Scene.TERMINAL_MAIN_THEME, Scene.INDEX)
@edge(Scene.TERMINAL_EPISODE, Scene.INDEX)
@edge(Scene.TERMINAL_BIOGRAPHY, Scene.INDEX)
@edge(Scene.TERMINAL_COLLECTION, Scene.INDEX)
@edge(Scene.TERMINAL_REGULAR, Scene.INDEX)
@edge(Scene.TERMINAL_LONGTERM, Scene.INDEX)
@edge(Scene.DEPOT, Scene.INDEX)
@edge(Scene.HEADHUNTING, Scene.INDEX)
@edge(Scene.MAIL, Scene.INDEX)
@edge(Scene.SIGN_IN_DAILY, Scene.INDEX)
def back_to_index(solver: BaseSolver):
    solver.back()


@edge(Scene.LEAVE_INFRASTRUCTURE, Scene.INDEX)
def leave_infrastructure(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=1)


@edge(Scene.DOWNLOAD_VOICE_RESOURCES, Scene.INDEX)
def dont_download_voice(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=0)


@edge(Scene.LOGIN_QUICKLY, Scene.INDEX)
def login_quickly(solver: BaseSolver):
    solver.tap_element("login_awake")


@edge(Scene.LOGIN_CAPTCHA, Scene.INDEX)
def login_captcha(solver: BaseSolver):
    solver.solve_captcha()
    solver.sleep(5)


@edge(Scene.LOGIN_BILIBILI, Scene.INDEX)
def login_bilibili(solver: BaseSolver):
    solver.tap((1000, 600))


@edge(Scene.EXIT_GAME, Scene.INDEX)
def exit_cancel(solver: BaseSolver):
    solver.tap_element("double_confirm/main", x_rate=0)


@edge(Scene.MATERIEL, Scene.INDEX)
def materiel(solver: BaseSolver):
    solver.tap((960, 960))


@edge(Scene.ANNOUNCEMENT, Scene.INDEX)
def announcement(solver: BaseSolver):
    solver.tap(config.recog.check_announcement())


@edge(Scene.AGREEMENT_UPDATE, Scene.INDEX)
def agreement(solver: BaseSolver):
    if pos := solver.find("read_and_agree"):
        solver.tap(pos)
    else:
        solver.tap((791, 728))
        solver.tap((959, 828))


@edge(Scene.INDEX, Scene.INFRA_MAIN)
def index_to_infra(solver: BaseSolver):
    solver.tap_index_element("infrastructure")


@edge(Scene.INDEX, Scene.BUSINESS_CARD)
def index_to_friend(solver: BaseSolver):
    solver.tap_index_element("friend")


@edge(Scene.INDEX, Scene.MISSION_DAILY)
def index_to_mission(solver: BaseSolver):
    solver.tap_index_element("mission")


@edge(Scene.INDEX, Scene.RECRUIT_MAIN)
def index_to_recruit(solver: BaseSolver):
    solver.tap_index_element("recruit")


@edge(Scene.INDEX, Scene.SHOP_OTHERS)
def index_to_shop(solver: BaseSolver):
    solver.tap_index_element("shop")


@edge(Scene.INDEX, Scene.TERMINAL_MAIN)
def index_to_terminal(solver: BaseSolver):
    solver.tap_index_element("terminal")


@edge(Scene.INDEX, Scene.DEPOT)
def index_to_depot(solver: BaseSolver):
    solver.tap_index_element("warehouse")


@edge(Scene.INDEX, Scene.MAIL)
def index_to_mail(solver: BaseSolver):
    solver.tap_index_element("mail")


@edge(Scene.INDEX, Scene.HEADHUNTING)
def index_to_headhunting(solver: BaseSolver):
    solver.tap_index_element("headhunting")

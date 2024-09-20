from arknights_mower.utils.solver import BaseSolver

from .utils import DG

# 终端

terminal_button = {
    501: "main",
    502: "main_theme",
    503: "intermezzi",
    504: "biography",
    505: "collection",
    506: "regular",
    507: "longterm",
    508: "contract",
}


def terminal_transition_factory(t):
    def terminal_transition(solver: BaseSolver):
        solver.tap_terminal_button(terminal_button[t])

    return terminal_transition


for s in range(501, 509):
    for t in range(501, 509):
        if t == s:
            continue
        DG.add_edge(s, t, transition=terminal_transition_factory(t))

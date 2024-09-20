from datetime import datetime

from arknights_mower.utils.graph import SceneGraphSolver

from .sign_in import SignIn


class SignInSolver(SceneGraphSolver):
    def run(self):
        success = True
        if datetime.now() < datetime(2024, 9, 22):
            success = success and SignIn().run()
        return success

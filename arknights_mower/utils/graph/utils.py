import functools

import networkx as nx

from arknights_mower.utils.csleep import MowerExit
from arknights_mower.utils.log import logger
from arknights_mower.utils.scene import Scene, SceneComment
from arknights_mower.utils.solver import BaseSolver

DG = nx.DiGraph()


def edge(v_from: int, v_to: int, interval: int = 1):
    def decorator(func):
        DG.add_edge(v_from, v_to, weight=interval, transition=func)

        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)

        return wrapper

    return decorator


class SceneGraphSolver(BaseSolver):
    def scene_graph_navigation(self, scene: int):
        """按场景图跳转到指定场景"""

        while self.scene() != scene:
            self.scene_graph_step(scene)

    def scene_graph_step(self, scene: int):
        """waiting_solver()或按场景图跳转到指定场景只操作一步"""
        if scene not in DG.nodes:
            logger.error(f"{SceneComment[scene]}不在场景图中")
            self.sleep()
            return

        if (current := self.scene()) in self.waiting_scene:
            if self.waiting_solver():
                return
            else:
                current = self.scene()

        if current == scene:
            return
        if current not in DG.nodes:
            logger.debug(f"{SceneComment[current]}不在场景图中")
            self.sleep(10)
            return
        try:
            sp = nx.shortest_path(DG, current, scene, weight="weight")
        except Exception as e:
            logger.exception(f"场景图路径计算异常：{e}")
            self.sleep(10)
            return

        logger.debug(sp)

        next_scene = sp[1]
        transition = DG.edges[current, next_scene]["transition"]
        try:
            transition(self)
        except MowerExit:
            raise
        except Exception as e:
            logger.exception(f"场景转移异常：{e}")
            self.sleep()

    def back_to_index(self):
        self.scene_graph_navigation(Scene.INDEX)

    def back_to_infrastructure(self):
        self.scene_graph_navigation(Scene.INFRA_MAIN)

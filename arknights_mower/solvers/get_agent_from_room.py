from datetime import datetime, timedelta

from arknights_mower import __main__
from arknights_mower.solvers.base_mixin import BaseMixin
from arknights_mower.solvers.enter_room import EnterRoomSolver
from arknights_mower.utils import config
from arknights_mower.utils.graph import SceneGraphSolver
from arknights_mower.utils.image import cropimg
from arknights_mower.utils.log import logger

name_x = (1288, 1869)
name_y = [(135, 326), (344, 535), (553, 744), (532, 723), (741, 932)]
name_p = [tuple(zip(name_x, y)) for y in name_y]
mood_x = (1470, 1780)
mood_y = [(219, 220), (428, 429), (637, 638), (615, 616), (823, 824)]
mood_p = [tuple(zip(mood_x, y)) for y in mood_y]
time_x = (1650, 1780)
time_y = [(270, 305), (480, 515), (690, 725), (668, 703), (877, 912)]
time_p = [tuple(zip(time_x, y)) for y in time_y]


class GetAgentFromRoomSolver(SceneGraphSolver, BaseMixin):
    def run(self, room: str, read_agent_time=False):
        """
        Args:
            room: 房间名
            read_agent_time: 读取工作或休息时间
        """
        self.room = room
        self.read_agent_time = read_agent_time
        self.index = 0
        self.result = []
        self.length = len(__main__.base_scheduler.op_data.plan[self.room])
        self.need_swipe = True if self.length > 3 else False
        self.wait_start()
        super().run()
        return self.result

    def timeout(self) -> bool:
        return datetime.now() > self.start_time + timedelta(seconds=3)

    def wait_start(self):
        self.start_time = datetime.now()

    def read_agent_data(self, index):
        data = {}
        if self.find("infra_no_operator", scope=name_p[index]):
            data["agent"] = ""
            data["mood"] = -1
        else:
            data["agent"] = self.read_screen(
                cropimg(config.recog.gray, name_p[index]), type="name"
            )
            data["mood"] = self.read_accurate_mood(
                cropimg(config.recog.gray, mood_p[index])
            )
            if self.read_agent_time:
                if data["mood"] == 24 or self.room in ["central", "meeting", "factory"]:
                    data["time"] = datetime.now()
                else:
                    data["time"] = self.double_read_time(time_p[index])
        self.result.append(data)

    def transition(self) -> bool:
        if self.detect_product_complete():
            logger.info("检测到产物收取提示")
            self.sleep(0.5)
        elif self.find("room_detail"):
            self.wait_start()
            if self.index >= 3 and self.need_swipe:
                if self.get_color((1800, 930))[0] > 51:
                    self.swipe(
                        (config.recog.w * 0.8, config.recog.h * 0.5),
                        (0, -config.recog.h * 0.45),
                        duration=500,
                        interval=1,
                    )
                elif self.timeout():
                    EnterRoomSolver().run(self.room)
                else:
                    self.need_swipe = False
            elif self.index == self.length:
                return True
            elif self.index < self.length:
                self.read_agent_data(self.index)
                self.index += 1
            else:
                EnterRoomSolver().run(self.room)
        else:
            EnterRoomSolver().run(self.room)

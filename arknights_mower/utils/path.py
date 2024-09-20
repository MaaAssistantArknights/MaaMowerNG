import os
from pathlib import Path

appname = "arknights_mower"
appauthor = "ArkMower"
# global_space：多开时global_space为多开数据目录

global_space = None

# install_dir：源码目录

_install_dir = Path(os.getcwd()).resolve()


def get_path(path: str) -> Path:
    """
    使用 '@xxx/' 来表示一些特别的目录
    @app: 多开数据目录, 例如 get_path('@app/log/runtime.log')
    @install: 源码目录
    """
    global global_space
    path = path.replace("\\", "/")

    if isinstance(path, str) and path.startswith("@"):
        index = path.find("/")
        index = index if index != -1 else len(path)
        special_dir_name = path[1:index]
        relative_path = path[index:].strip("/")
        if special_dir_name == "app":
            return (
                Path(_install_dir) / relative_path
                if global_space is None
                else Path(global_space) / relative_path
            )
        elif special_dir_name == "install":
            return Path(_install_dir) / relative_path
        else:
            raise ValueError(
                "{}: {} 不是一个有效的特殊目录别名".format(path, special_dir_name)
            )
    else:
        return Path(path)
        # raise ValueError("{} 路径必须以 '@xxx' 开头".format(path))

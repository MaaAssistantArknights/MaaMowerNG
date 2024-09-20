import platform
from pathlib import Path

__version__ = "ng"


__rootdir__ = Path(__file__).parent.resolve()

from arknights_mower.utils.git_rev import revision_info

__version__ += "+" + revision_info()[:7]

__system__ = platform.system().lower()

from arknights_mower.utils import config
from arknights_mower.utils.email import send_message
from arknights_mower.utils.log import logger


def notify(msg, level="INFO"):
    logger.info(msg)
    send_message(msg, level=level, attach_image=config.recog.img)

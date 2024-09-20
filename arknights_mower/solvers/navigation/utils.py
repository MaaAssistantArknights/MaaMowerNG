import string
from typing import Literal

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from arknights_mower.utils import typealias as tp
from arknights_mower.utils.image import cropimg


def generate_name(
    name: str,
    font_size: int = 40,
    style: Literal["light", "dark"] = "light",
    draw: bool = False,
) -> tp.GrayImage:
    """生成思源黑体的关卡名图片

    Args:
        name: 关卡名
        font_size: 字号
        style: 亮/暗
        draw: 调试时显示结果
    """
    font = ImageFont.truetype(
        "arknights_mower/fonts/SourceHanSansCN-Medium.otf", font_size
    )
    img = Image.new(mode="L", size=(250, 100))
    ImageDraw.Draw(img).text((20, 0), name, fill=(255,), font=font)
    img = np.array(img, dtype=np.uint8)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rect = [cv2.boundingRect(c) for c in contours]
    left = min(x for x, y, w, h in rect)
    right = max(x + w for x, y, w, h in rect)
    top = min(y for x, y, w, h in rect)
    bottom = max(y + h for x, y, w, h in rect)
    img = cropimg(img, ((left, top), (right, bottom)))
    if style == "light":
        img = cv2.bitwise_not(img)

    if draw:
        from matplotlib import pyplot as plt

        plt.imshow(img, cmap="gray", vmin=0, vmax=255)
        plt.show()

    return img


last_letters = {}
for i in list(range(10)) + list(string.ascii_uppercase):
    i = str(i)
    last_letters[i] = generate_name(i, 42)

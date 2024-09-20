from concurrent.futures import ThreadPoolExecutor
from functools import partial

import cv2

from arknights_mower.models import avatar, portrait
from arknights_mower.utils import config
from arknights_mower.utils import typealias as tp
from arknights_mower.utils.image import cropimg, thres2
from arknights_mower.utils.log import logger
from arknights_mower.utils.matcher import GOOD_DISTANCE_LIMIT, flann, keypoints
from arknights_mower.utils.vector import va


def segment_room_select(img: tp.Image) -> list[tp.Scope]:
    "基建房间内选干员"
    line1 = cropimg(img, ((600, 519), (1920, 520)))
    hsv = cv2.cvtColor(line1, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (98, 140, 200), (102, 255, 255))
    line1 = cv2.cvtColor(line1, cv2.COLOR_RGB2GRAY)
    line1[mask > 0] = (255,)
    line1 = thres2(line1, 140)

    last_line = line1[-1]
    prev = last_line[0]
    start = None
    name_x = []
    for i in range(1, line1.shape[1]):
        curr = last_line[i]
        if prev == 0 and curr == 255 and start and i - start > 186:
            name_x.append((i + 450, i + 570))
        elif prev == 255 and curr == 0:
            start = i
        prev = curr

    avatar_y = ((180, 310), (600, 730))
    avatar_p = []
    for x in name_x:
        for y in avatar_y:
            avatar_p.append(tuple(zip(x, y)))

    logger.debug(avatar_p)
    return avatar_p


def segment_team(img: tp.Image) -> list[tp.Scope]:
    "编队界面"
    # TODO: 利用img判断编队缺人的情况
    result = []
    for i in range(6):
        x = 310 + 232 * i
        for y in [180, 610]:
            result.append(((x, y), va((x, y), (120, 120))))
    logger.debug(result)
    return result


def segment_team_select(img: tp.Image) -> list[tp.Scope]:
    "作战编队和训练位选干员"
    line1 = cropimg(img, ((600, 510), (1920, 511)))
    hsv = cv2.cvtColor(line1, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, (98, 140, 200), (102, 255, 255))
    line1 = cv2.cvtColor(line1, cv2.COLOR_RGB2GRAY)
    line1[mask > 0] = (255,)
    line1 = thres2(line1, 140)
    last_line = line1[-1]
    prev = last_line[0]
    start = None
    name_x = []
    for i in range(1, line1.shape[1]):
        curr = last_line[i]
        if prev == 0 and curr == 255 and start and i - start > 96:
            name_x.append((i + 450, i + 570))
        elif prev == 255 and curr == 0:
            start = i
        prev = curr

    avatar_y = ((170, 290), (585, 705))
    avatar_p = []
    for x in name_x:
        for y in avatar_y:
            avatar_p.append(tuple(zip(x, y)))

    logger.debug(avatar_p)
    return avatar_p


p_list = []
for i, img_list in portrait.items():
    p_list.extend(img_list)

a_list = []
for i, img_list in avatar.items():
    a_list.extend(img_list)


def match_operator(
    gray: tp.GrayImage, segment: list[tp.Scope], model: dict, d_list: list
) -> tuple[tuple[str, tp.Scope]]:
    avatar_p = {}
    for av in segment:
        avatar_p[av] = None, 0

    kp, des = keypoints(gray)

    match = partial(flann.knnMatch, trainDescriptors=des, k=2)

    with ThreadPoolExecutor(max_workers=config.conf.max_workers) as executor:
        result = executor.map(match, d_list)

    for i, img_list in model.items():
        for d1 in img_list:
            matches = next(result)
            good = {}
            for j in avatar_p:
                good[j] = []
            for pair in matches:
                if len(pair) != 2:
                    continue
                x, y = pair
                if x.distance >= GOOD_DISTANCE_LIMIT * y.distance:
                    continue
                for j in avatar_p:
                    kpj = kp[x.trainIdx]
                    if j[0][0] < kpj.pt[0] < j[1][0] and j[0][1] < kpj.pt[1] < j[1][1]:
                        good[j].append(x)
            for j, g in good.items():
                score = len(g) / len(d1)
                if avatar_p[j][1] < score:
                    avatar_p[j] = i, score

    op_name = [p[0] for p in avatar_p.values()]
    logger.debug(op_name)

    return tuple(zip(op_name, segment))


match_portrait = partial(match_operator, model=portrait, d_list=p_list)
match_avatar = partial(match_operator, model=avatar, d_list=a_list)


def operator_room_select(img: tp.Image) -> tuple[tuple[str, tp.Scope]]:
    "基建房间内选干员"
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return match_portrait(gray, segment_room_select(img))


def operator_team(img: tp.Image) -> tuple[tuple[str, tp.Scope]]:
    "编队界面"
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return match_portrait(gray, segment_team(img))


def operator_team_select(img: tp.Image) -> tuple[tuple[str, tp.Scope]]:
    "作战编队和训练位选干员"
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return match_portrait(gray, segment_team_select(img))

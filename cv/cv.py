import cv2
from cv.template import templateMatching
from cv.keypoint import KAZEMatching


def saveSupporter(device):
    # 1.读取图片
    screen = device.screenshot(format="opencv")
    # 2.截取图片
    supporter1, supporter2 = screen[190:278, 60:148], screen[310:398, 60:148]
    # 3.保存图片
    cv2.imwrite("img/supporter/1.png", supporter1)
    cv2.imwrite("img/supporter/2.png", supporter2)


def getMatchingPos(filename, device, threshold=0.9, targetPos=5, method="tpl"):
    if method == "tpl":
        return templateMatching(filename, device, threshold, targetPos)
    elif method == "kaze":
        return KAZEMatching(filename, device, threshold, targetPos)
    else:
        return None

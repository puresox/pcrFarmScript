import cv2


def getPos(leftTopPos, w, h, targetPos):
    (leftTopPosX, leftTopPosY) = leftTopPos
    pos = leftTopPos
    if targetPos == 1:
        pos = (leftTopPosX, leftTopPosY + h)
    elif targetPos == 2:
        pos = (int(leftTopPosX + w / 2), leftTopPosY + h)
    elif targetPos == 3:
        pos = (leftTopPosX + w, leftTopPosY + h)
    elif targetPos == 4:
        pos = (leftTopPosX, int(leftTopPosY + h / 2))
    elif targetPos == 6:
        pos = (leftTopPosX + w, int(leftTopPosY + h / 2))
    elif targetPos == 7:
        pos = pos
    elif targetPos == 8:
        pos = (int(leftTopPosX + w / 2), leftTopPosY)
    elif targetPos == 9:
        pos = (leftTopPosX + w, leftTopPosY)
    else:
        pos = (int(leftTopPosX + w / 2), int(leftTopPosY + h / 2))
    return pos


def templateMatching(filename, device, threshold=0.9, targetPos=5):
    """模板匹配,返回结果

    Args:
        filename (string): 模板图文件名称
        device (object): uiautomator2对象
        threshold (float, optional): 阈值. Defaults to 0.9.
        targetPos (int, optional): 点击位置. Defaults to 5.

    Returns:
        tuple: 返回坐标或none
    """
    # 1.读取图片
    imSearch = device.screenshot(format="opencv")
    imTpl = cv2.imread("img/{name}".format(name=filename))
    h, w = imTpl.shape[:2]
    # 2.模板匹配
    res = cv2.matchTemplate(imSearch, imTpl, cv2.TM_CCOEFF_NORMED)
    # 3.获取匹配结果
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
    confidence = maxVal  # 可信度
    if confidence <= threshold:
        return None
    # 4.标记匹配结果
    # cv2.rectangle(
    #     imSearch, maxLoc, (maxLoc[0] + w, maxLoc[1] + h), (0, 255, 0), 3,
    # )
    # cv2.imshow("res", imSearch)
    # cv2.waitKey(1000)
    # cv2.destroyAllWindows()
    # 5.求点击位置
    pos = getPos(maxLoc, w, h, targetPos)
    return pos


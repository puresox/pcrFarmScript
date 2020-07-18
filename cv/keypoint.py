import cv2
import numpy as np

# import uuid


def getKeyPoints(imSearch, imSource):
    """根据传入图像,计算图像所有的特征点,并得到匹配特征点对."""
    # 准备工作: 初始化算子
    detector = cv2.KAZE_create()
    # 获取特征点集，并匹配出特征点对
    kpSch, desSch = detector.detectAndCompute(imSearch, None)
    kpSrc, desSrc = detector.detectAndCompute(imSource, None)
    # flann
    flann = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
    matches = flann.knnMatch(desSch, desSrc, 2)
    # good为特征点初选结果，剔除掉前两名匹配太接近的特征点，不是独特优秀的特征点直接筛除(多目标识别情况直接不适用)
    ratioThresh = 0.75
    good = []
    for m, n in matches:
        if m.distance < ratioThresh * n.distance:
            good.append(m)
    # good点需要去除重复的部分，（设定源图像不能有重复点）去重时将src图像中的重复点找出即可
    # 去重策略：允许搜索图像对源图像的特征点映射一对多，不允许多对一重复（即不能源图像上一个点对应搜索图像的多个点）
    good_diff, diff_good_point = [], [[]]
    for m in good:
        diff_point = [int(kpSrc[m.trainIdx].pt[0]), int(kpSrc[m.trainIdx].pt[1])]
        if diff_point not in diff_good_point:
            good_diff.append(m)
            diff_good_point.append(diff_point)
    good = good_diff

    return kpSch, kpSrc, good


def handleGoodPoints(kpSch, kpSrc, good, imSearch, imSource):
    if len(good) < 4:
        return None
    else:
        """特征点匹配点对数目>=4个，可使用单矩阵映射,求出识别的目标区域."""
        schPts, imgPts = (
            np.float32([kpSch[m.queryIdx].pt for m in good]).reshape(-1, 1, 2),
            np.float32([kpSrc[m.trainIdx].pt for m in good]).reshape(-1, 1, 2),
        )
        # M是转化矩阵
        M, mask = cv2.findHomography(schPts, imgPts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        # 从good中间筛选出更精确的点(假设good中大部分点为正确的，由ratio=0.7保障)
        selected = [v for k, v in enumerate(good) if matchesMask[k]]

        # 针对所有的selected点再次计算出更精确的转化矩阵M来
        schPts, imgPts = (
            np.float32([kpSch[m.queryIdx].pt for m in selected]).reshape(-1, 1, 2),
            np.float32([kpSrc[m.trainIdx].pt for m in selected]).reshape(-1, 1, 2),
        )
        M, mask = cv2.findHomography(schPts, imgPts, cv2.RANSAC, 5.0)
        # 计算四个角矩阵变换后的坐标，也就是在大图中的目标区域的顶点坐标:
        h, w = imSearch.shape[:2]
        h_s, w_s = imSource.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(
            -1, 1, 2
        )
        dst = cv2.perspectiveTransform(pts, M)

        # trans numpy arrary to python list: [(a, b), (a1, b1), ...]
        def cal_rect_pts(dst):
            return [tuple(npt[0]) for npt in dst.astype(int).tolist()]

        pypts = cal_rect_pts(dst)
        # 注意：虽然4个角点有可能越出source图边界，但是(根据精确化映射单映射矩阵M线性机制)中点不会越出边界
        lt, br = pypts[0], pypts[2]
        middlePoint = int((lt[0] + br[0]) / 2), int((lt[1] + br[1]) / 2)
        # 考虑到算出的目标矩阵有可能是翻转的情况，必须进行一次处理，确保映射后的“左上角”在图片中也是左上角点：
        xMin, xMax = min(lt[0], br[0]), max(lt[0], br[0])
        yMin, yMax = min(lt[1], br[1]), max(lt[1], br[1])
        # 挑选出目标矩形区域可能会有越界情况，越界时直接将其置为边界：
        # 超出左边界取0，超出右边界取w_s-1，超出下边界取0，超出上边界取h_s-1
        # 当x_min小于0时，取0。  x_max小于0时，取0。
        xMin, xMax = int(max(xMin, 0)), int(max(xMax, 0))
        # 当x_min大于w_s时，取值w_s-1。  x_max大于w_s-1时，取w_s-1。
        xMin, xMax = int(min(xMin, w_s - 1)), int(min(xMax, w_s - 1))
        # 当y_min小于0时，取0。  y_max小于0时，取0。
        yMin, yMax = int(max(yMin, 0)), int(max(yMax, 0))
        # 当y_min大于h_s时，取值h_s-1。  y_max大于h_s-1时，取h_s-1。
        yMin, yMax = int(min(yMin, h_s - 1)), int(min(yMax, h_s - 1))
        # 目标区域的角点，按左上、左下、右下、右上点序：(x_min,y_min)(x_min,y_max)(x_max,y_max)(x_max,y_min)
        pts = np.float32(
            [[xMin, yMin], [xMin, yMax], [xMax, yMax], [xMax, yMin]]
        ).reshape(-1, 1, 2)
        pypts = cal_rect_pts(pts)

        return middlePoint, pypts, [xMin, xMax, yMin, yMax, w, h]


def KAZEMatching(filename, device, threshold=0.9, targetPos=5):
    # 1.读取图片
    imSearch = cv2.imread("img/{name}".format(name=filename))
    imSource = device.screenshot(format="opencv")
    # 2.获取特征点集并匹配出特征点对
    kpSch, kpSrc, good = getKeyPoints(imSearch, imSource)
    # 3.根据匹配点对(good),提取出来识别区域:
    originResult = handleGoodPoints(kpSch, kpSrc, good, imSearch, imSource)
    # 某些特殊情况下直接返回None作为匹配结果:
    if originResult is None:
        return None
    else:
        middlePoint, pypts, posRange = originResult
        return middlePoint

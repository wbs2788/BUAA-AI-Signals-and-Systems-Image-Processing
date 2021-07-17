# 模块导入
import cv2
import numpy as np
import sys
import importlib


def get_skin_yuv(img):  # 获得图像yuv色彩空间值，并做二值化与腐蚀处理，使美颜操作仅对人脸部分实现
    ycrcb_img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    (y, cr, cb) = cv2.split(ycrcb_img)
    (x, y) = cr.shape
    (xt, yt, zt) = img.shape
    tag = np.zeros((xt, yt), int)
    back = np.zeros(img.shape, np.uint8)
    for i in range(x):
        for j in range(y):
            if (cr[i][j] > 133) and (cr[i][j] < 173) and (cb[i][j] > 77) and (cb[i][j] < 127) and (tag[i][j] == 0):
                for i1 in range(0, 1):  # 这里的range是腐蚀大小，在人脸美颜中开过大会导致锯齿化
                    for j1 in range(0, 1):
                        if (i + i1 < x) and (j + j1 < y):
                            if tag[i + i1][j + j1] == 0:
                                tag[i + i1][j + j1] = 1
                                back[i + i1][j + j1] = img[i + i1][j + j1]
                                img[i + i1][j + j1] = 0  # 二值化+腐蚀
    return back


def nothing(x):
    pass

print("Press 'Q' or space to exit")

while True:  # 选择功能
    func = int(input("choose function:\n1:Beautify\n2:Detection\n"))
    if func == 1 or 2:
        break


# 选择照片路径
imagepath = input("type which pic\n")

if func == 1:
    print("Beautifying\n")
    img = cv2.imread(imagepath, 1)

    fsize = [0, 0]  # 进行压缩（照片像素太高）
    for i, l in enumerate(img.shape[:2]):
        fsize[i] = int(l/4)
    fsize = fsize[::-1]
    img = cv2.resize(img, fsize)
    old_wlx = cv2.resize(img, fsize)  # 原图，比较用

    cv2.namedWindow('result')  # 建立简单的交互，拖动条对应双边滤波的参数
    cv2.createTrackbar('d', 'result', 0, 50, nothing)
    cv2.createTrackbar('sigmaColor', 'result', 0, 255, nothing)
    cv2.createTrackbar('sigmaSpace', 'result', 0, 255, nothing)
    a = cv2.getTrackbarPos('d', 'result')
    b = cv2.getTrackbarPos('sigmaColor', 'result')
    c = cv2.getTrackbarPos('sigmaSpace', 'result')

    back0 = get_skin_yuv(img)  # 获取提取人脸肤色的img

    img0 = np.zeros(img.shape, np.uint8)  # 定义一些底片
    infmg_1 = np.zeros(img.shape, np.uint8)
    infmg_2 = np.zeros(img.shape, np.uint8)
    infmg_3 = np.zeros(img.shape, np.uint8)
    infmg_4 = np.zeros(img.shape, np.uint8)

    while (1):
        key = cv2.waitKey(1)
        if key > 0:
            break

        a2 = cv2.getTrackbarPos('d', 'result')
        b2 = cv2.getTrackbarPos('sigmaColor', 'result')
        c2 = cv2.getTrackbarPos('sigmaSpace', 'result')

        if a2 != a or b2 != b or c2 != c:
            cv2.bilateralFilter(back0, a, b, c, infmg_1)  # 双边滤波
            a, b, c = a2, b2, c2
            dst1 = infmg_1 - back0 + 128
            # cv2.imshow("Bliateral", dst1)

            infmg_2 = cv2.GaussianBlur(dst1, (1, 1), 0, 0)  # 高斯滤波
            infmg_3 = back0 + 2*infmg_2 - 255
            # cv2.imshow("Gauss", infmg_3)

            infmg_4 = cv2.addWeighted(back0, 0.2, infmg_3, 0.8, 0)  # 加权相加
            img0 = cv2.add(img, infmg_4)

            window = np.hstack([img0, old_wlx])  # 展示
            cv2.imshow('result', window)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.imwrite("result.jpg", img0)  # 将结果进行存储
    cv2.destroyAllWindows()

if func == 2:  # 尝试了其他同学使用的级联器
    importlib.reload(sys)
    pathf = 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(pathf)
    img = cv2.imread(imagepath)
    fsize = [0, 0]
    for i, l in enumerate(img.shape[:2]):
        fsize[i] = int(l/1)
    fsize = fsize[::-1]
    img = cv2.resize(img, fsize)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.15,
        minNeighbors = 5,
        minSize = (5, 5),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    print("发现{0}张人脸!".format(len(faces)))

    for (x, y, w, h) in faces:
        cv2.circle(img, ((x + x + w)//2, (y + y + h)//2), w//2, (0, 255, 0), 2)
    cv2.imshow("find{0}faces!", img)
    cv2.waitKey(0)

#模块导入
import cv2
import numpy as np
import os
from copy import *
from math import *

#变量与常量定义

try:
    os.remove("result.jpg")
except:FileNotFoundError
try:
    os.remove("noise.jpg")
except:FileNotFoundError

#加噪
peppers = cv2.imread("test.jpg", 0)
cv2.imwrite("gray.jpg",peppers)
row, column = peppers.shape
mul = row * column
noise_pepper = np.random.randint(0, 256, (row, column))
rand = 0.5
noise_pepper = np.where(noise_pepper < rand * 256, -255, 0)
peppers.astype("float")
noise_pepper.astype("float")
pepper = peppers + noise_pepper
pepper = np.where(pepper < 0, 0, pepper)


#输出加噪后图像

cv2.imwrite('noise.jpg',pepper)
img = copy(pepper)
img.astype("float")
result = copy(img)
result.astype("float")


#去噪
for t in range(3):            
    for i in range(0,row):
        for j in range(0,column):
            if img[i][j]==0:
                s = 0
                k = 0
                for m in range(-1,2):
                    for n in range(-1,2):
                        if img[min(i+m,row-1)][min(j+n,column-1)]!=0:
                            s = s + img[min(i+m,row-1)][min(j+n,column-1)]
                            k = k + 1
                        if k!=0:
                            result[i][j] = s/k
    img = copy(result)





#输出处理后图像
cv2.imwrite('result.jpg',result)
test = cv2.imread("test.jpg", 0)
cv2.imshow("gray", test.astype("uint8"))
cv2.imshow("noise", pepper.astype("uint8"))
cv2.imshow("result", result.astype("uint8"))

    





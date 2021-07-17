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
img = cv2.imread("test.jpg", 0)
cv2.imwrite("gray.jpg",img)
row, column = img.shape
mul = row*column
img.astype("float")
Gauss_noise = np.random.normal(0, 30, (row, column))
Gauss = img + Gauss_noise
Gauss = np.where(Gauss < 0, 0, np.where(Gauss > 255, 255, Gauss))

#输出加噪后图像

cv2.imwrite('noise.jpg',Gauss)
img = copy(Gauss)
img.astype("float")


#傅里叶变换
imarr = np.array(img)
img = np.fft.fft2(imarr)
img = np.fft.fftshift(img)
#Butterworth低通滤波去噪
D0 = 12.5
n = 0.9
for i in range(row):
    for j in range(column):
        img[i][j] = img[i][j]/(1+pow((pow(i-row/2,2)+pow(j-column/2,2))/pow(D0,2),n))

#傅里叶逆变换

img = np.fft.ifftshift(img)
ifft = np.fft.ifft2(img)
ifft = np.real(ifft)
max_v = np.max(ifft)
min_v = np.min(ifft)

for i in range(row):
	for j in range(column):
		img[i][j] = 255 * (ifft[i][j] - min_v)/(max_v - min_v)

img = np.real(img)
result = copy(img)






#锐化
La = [[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]
for t in range(1):
    for i in range(1,row-1):
        for j in range(1,column-1):
            s = 0
            for m in range(0,3):
                for n in range(0,3):
                    s = s + La[m][n]*img[i+m-1][j+n-1]
            if s>255:
                result[i][j] = 255
            elif s<0:
                result[i][j] = 0
            else:
                result[i][j] = s
    








#输出处理后图像
cv2.imwrite('result.jpg',result)
test = cv2.imread("test.jpg", 0)
cv2.imshow("noise", Gauss.astype("uint8"))
cv2.imshow("result", result.astype("uint8"))

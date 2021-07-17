# 详细内容见实验报告

# "椒盐去噪.py"和"高斯去噪.py"的使用方法

1.将要处理的图像命名为test.jpg并与"椒盐去噪.py"（或"高斯去噪.py"）置于同一目录下，然后用IDE打开"椒盐去噪.py"（或"高斯去噪.py"）运行（直接双击py运行仿佛没有效果），会在同一目录下输出

gray.jpg(test.jpg的灰度图)

noise.jpg(加入噪声的图像)

result.jpg(去噪结果)

2.调用的模块有cv2，numpy，os，copy，math

# **FaceBeautify.py** **使用方法**

```python
import cv2 
import numpy as np 
import sys 
import importlib
```

级联器：haarcascade_frontalface_default.xml

打开后，选择功能，输入当前目录下需要进行处理的图像的文件名。该程序的脸部检测使用级联器实现。

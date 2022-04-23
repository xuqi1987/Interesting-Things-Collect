# -*- coding: UTF-8 -*-
#!/usr/bin/env python
import cv2
from PIL import Image as image
from pylab import *
import numpy as np
import matplotlib.pyplot as plt

#img = cv2.imread("/Users/xuqi/Documents/1.jpg")

# 取的设备编号为0的
cap = cv2.VideoCapture(0)

ret, frame = cap.read()

pil_img = image.fromarray(frame)

# frame = cv2.imencode('.jpg', frame)[1].tostring()


plt.imshow(pil_img)

x = np.arange(0, 5, 0.1);
y = np.sin(x)
plt.plot(x, y)

plt.show()






# img = cv2.imread("test.jpg")
#
# cv2.namedWindow("Image")
#
# cv2.imshow("Image", img)
#
# cv2.waitKey (0)
#
# cv2.destroyAllWindows()
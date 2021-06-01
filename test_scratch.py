
import numpy as np
import cv2
import random as rng
import math

def areaCal(contour):

    area = 0
    for i in range(len(contour)):
        area += cv2.contourArea(contour[i])

    return area

frame=cv2.imread('0297.jpg')
sp=frame.shape
data_A = np.zeros([sp[0], sp[1]], np.uint8)
#out = cv2.VideoWriter('output_92.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, size,1)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 230, 255, 0)  # 二值化
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)  # 开运算
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)  # 闭运算
contours, hierarchy = cv2.findContours(closing, 3, 1)
for i in range(len(contours)):
    color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
    a=cv2.drawContours(frame, contours,i,color)

print(areaCal(contours))
th_=178
cx=163
cy=162
a=26
b=40
frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)  # 在原图中画轮廓
image=cv2.ellipse(frame,(cx,cy),(a, b), th_, 0, 360, (0, 0, 255), 2, 8, 0)
for i in range(0, sp[0]):
    for j in range(0, sp[1]):
        # print(int(i*cos)+int(j*sin),cx,int(-i*sin)+int(j*cos),cy,a,b)
        th = math.pi * th_ / 180
        cos = math.cos(th)
        sin = math.sin(th)
        print(i,j)

        if math.pow((int(i-cx)*cos+int(j-cy)*sin),2)/(a*a)+math.pow((int(j-cy)*cos-int(i-cx)*sin),2)/(b*b)<=0.25:  # 长轴为x轴，且像素点在方框内
            data_A[i][j] += 1  # 若在椭圆内，则对该像素点进行累加
cv2.imwrite('00001-%d.jpg' %th_, image)
#for c in range(len(contours)):

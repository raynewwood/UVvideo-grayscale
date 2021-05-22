import numpy as np
import cv2
import math

font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
cap = cv2.VideoCapture('c01.avi')
# Define the codec and create VideoWriter object
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, size,1)
nihe =4
#1 圆拟合
#2 直边界矩形
#3 最小矩形
#4 椭圆

# 计算(x1,y1)(x,y)、(x2,y2)(x,y)向量的叉乘
def GetCross(x1,y1,x2,y2,x,y):
    a=(x2-x1,y2-y1)
    b=(x-x1,y-y1)
    return a[0]*b[1]-a[1]*b[0]

# 判断(x,y)是否在矩形内部
def isInSide(x1,y1,x2,y2,x3,y3,x4,y4,x,y):
    return GetCross(x1,y1,x2,y2,x,y)*GetCross(x3,y3,x4,y4,x,y)>=0 and GetCross(x2,y2,x3,y3,x,y)*GetCross(x4,y4,x1,y1,x,y)>=0
f=0
count=1
data_A = np.zeros([448, 448], np.uint8)
while(cap.isOpened()):
    ret, frame = cap.read()
    if nihe ==1: #圆拟合
        if ret==True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化
            ret, thresh = cv2.threshold(gray, 230, 255, 0)  # 二值化
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算
            contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测
            for c in range(len(contours)):
                (x, y), radius = cv2.minEnclosingCircle(contours[c])
                center = (int(x), int(y))
                radius = int(radius)
                area = cv2.contourArea(contours[c])
                equi_diameter = np.sqrt(4 * area / np.pi)
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                text1 = 'Center: (' + str(int(x)) + ', ' + str(int(y)) + ') '
                text2 = 'Diameter: ' + str(2 * radius)
                for i in range(0,size[0]):
                    for j in range(0,size[1]):
                        if (i-x)*(i-x)+(j-y)*(j-y)<radius*radius:#判断该像素点是否在圆内
                            data_A[i][j]+=1#若在圆内，则将该像素点置1
                cv2.putText(frame, text1, (10, 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                cv2.putText(frame, text2, (10, 60), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                out.write(frame)
                cv2.imshow('frame',frame)
                # 若没有按下q键，则每1毫秒显示一帧
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        else:
            break



    elif nihe ==2:#2 直边界矩形
        if ret==True:
            #frame = cv2.flip(frame,0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化
            ret, thresh = cv2.threshold(gray, 230, 255, 0)  # 二值化
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算
            contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测
            for c in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[c])
                area = cv2.contourArea(contours[c])
                aspect_ratio = float(w) / h  # 长宽比
                rect_area = w * h
                extent = float(area) / rect_area  # 轮廓面积与边界矩形面积的比
                hull = cv2.convexHull(contours[c])
                hull_area = cv2.contourArea(hull)
                solidity = float(area) / hull_area  # 轮廓面积与凸包面积的比。
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text1 = 'Aspect Ration: ' + str(round(aspect_ratio, 4))
                text2 = 'Extent:  ' + str(round(extent, 4))
                text3 = 'Solidity: ' + str(round(solidity, 4))
                for i in range(0,size[0]):
                    for j in range(0,size[1]):
                        if (i>=x) and (i<=x+w):
                            if  (j>=y) and(j<=y+h):#如果像素点在方框内
                                data_A[i][j]+=1#若在矩形内，则对该像素点进行累加

                cv2.putText(frame, text1, (10, 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                cv2.putText(frame, text2, (10, 60), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                cv2.putText(frame, text3, (10, 90), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                out.write(frame)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break
            
    elif nihe ==3:#3 最小矩形
        if ret==True:
            #frame = cv2.flip(frame,0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化
            ret, thresh = cv2.threshold(gray, 230, 255, 0)  # 二值化
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算
            contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测
            for c in range(len(contours)):
                rect = cv2.minAreaRect(contours[c])
                box = cv2.boxPoints(rect)
                box = np.int0(box)  # 获得矩形角点
                #计算各个点的坐标
                l_x = np.min(box[:, 0])
                r_x = np.max(box[:, 0])
                t_y = np.min(box[:, 1])
                b_y = np.max(box[:, 1])

                l_y = box[:, 1][np.where(box[:, 0] == l_x)][0]
                r_y = box[:, 1][np.where(box[:, 0] == r_x)][0]
                t_x = box[:, 0][np.where(box[:, 1] == t_y)][0]
                b_x = box[:, 0][np.where(box[:, 1] == b_y)][0]

                area = cv2.contourArea(box)
                width = rect[1][0]
                height = rect[1][1]
                cv2.polylines(frame, [box], True, (0, 255, 0), 3)#原画中画轮廓
                text1 = 'Width: ' + str(int(width)) + ' Height: ' + str(int(height))
                text2 = 'Rect Area: ' + str(area)
                for i in range(0,size[0]):
                    for j in range(0,size[1]):
                        if isInSide(l_x,l_y,r_x,r_y,t_x,t_y,b_x,b_y,i,j):#如果像素点在矩形内
                            data_A[i][j]+=1#若在圆内，则对该像素点进行累加

                #print('data=',data)
                cv2.putText(frame, text1, (10, 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                cv2.putText(frame, text2, (10, 60), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA, 0)
                out.write(frame)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break

    elif nihe ==4:#4 椭圆
        if ret==True:
            #frame = cv2.flip(frame,0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化
            ret, thresh = cv2.threshold(gray, 230, 255, 0)  # 二值化
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算
            contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测

            for c in range(len(contours)):
                (cx,cy),(a,b),angle = cv2.fitEllipse(contours[c])#（x, y）代表椭圆中心点的位置
                                                                 #（a, b）代表长短轴长度，应注意a、b为长短轴的直径，而非半径
                                                                 # #angle 代表了中心旋转的角度
                th = 2 * math.pi * angle / 360
                cos = math.cos(th)
                sin = math.sin(th)
                if a>=b:#判断长轴在x上还是Y上，若a>=b 则在x轴上，反之在y轴上
                    change=0
                else:
                    change=1
                print(change)
                cv2.ellipse(frame,(np.int32(cx),np.int32(cy)),
                            (np.int32(a/2), np.int32(b/2)), angle, 0, 360, (0, 0, 255), 2, 8, 0)
                for i in range(0,size[0]):
                    for j in range(0,size[1]):
                        if change ==0 and math.pow((i*cos+j*sin-cx),2)/(a*a)+math.pow((-i*sin+j*cos-cy),2)/(b*b)<=0.25:#长轴为x轴，且像素点在方框内
                            data_A[i][j]+=1#若在圆内，则对该像素点进行累加
                        elif change ==1 and math.pow((i*cos+j*sin-cx),2)/(b*b)+math.pow((-i*sin+j*cos-cy),2)/(a*a)<=0.25:#长轴为y轴，且像素点在方框内
                            data_A[i][j]+=1

                frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)#在原图中画轮廓
            #第一个参数是指明在哪幅图像上绘制轮廓；
            #第二个参数是轮廓本身，在Python中是一个list。
            #第三个参数指定绘制轮廓list中的哪条轮廓，如果是-1，则绘制其中的所有轮廓。
            # write the flipped frame
                out.write(frame)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break
    else:
        break
cap.release()
out.release()
cv2.destroyAllWindows()

import numpy as np
import cv2
import math


input='1s'
nihe =1
#1 圆拟合
#2 直边界矩形
#3 最小矩形
#4 最小椭圆
font = cv2.FONT_HERSHEY_SIMPLEX  # 设置字体样式
cap = cv2.VideoCapture('%s.mp4'%input)
# Define the codec and create VideoWriter object
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('output%s.mp4'%input, cv2.VideoWriter_fourcc(*'XVID'), 20.0, size,1)
threshold=size[0]*size[1]/1500
f=0
count=1
size_w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
size_h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
data_A = np.zeros([size_w, size_h], np.uint8)
while(cap.isOpened()):
    ret, frame = cap.read()
    if nihe ==1: #圆拟合
        if ret==True:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化
            ret, thresh = cv2.threshold(gray, 240, 255, 0)  # 二值化
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算
            contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测
            for c in range(len(contours)):
                if cv2.contourArea(contours[c])< threshold:
                    continue
                (x, y), radius = cv2.minEnclosingCircle(contours[c])
                center = (int(x), int(y))
                radius = int(radius)
                area = cv2.contourArea(contours[c])
                equi_diameter = np.sqrt(4 * area / np.pi)
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                text1 = 'Center: (' + str(int(x)) + ', ' + str(int(y)) + ') '
                text2 = 'Diameter: ' + str(2 * radius)
                for i in range(0,size_w):
                    for j in range(0,size_h):
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
                if cv2.contourArea(contours[c])< threshold:
                    continue
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
                if cv2.contourArea(contours[c])< threshold:
                    continue
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
                th = 2 * math.pi * rect[2] / 360
                cos = math.cos(th)
                sin = math.sin(th)
                minx=int(l_x*cos+l_y*sin)
                maxx=int(r_x*cos+r_y*sin)
                miny=int(-b_x*sin+b_y*cos)
                maxy=int(-t_x*sin+t_y*cos)

                area = cv2.contourArea(box)
                width = rect[1][0]
                height = rect[1][1]
                cv2.polylines(frame, [box], True, (0, 255, 0), 3)#原画中画轮廓
                text1 = 'Width: ' + str(int(width)) + ' Height: ' + str(int(height))
                text2 = 'Rect Area: ' + str(area)
                for i in range(0,size[0]):
                    for j in range(0,size[1]):
                        x=int(i*cos+j*sin)
                        y=int(-i*sin+j*cos)
                        #print(x,minx,maxx,y,miny,maxy)
                        if x<=maxx and x>=minx and y >=maxy and y<=miny:#如果像素点在矩形内
                            data_A[i][j]+=1#若在圆内，则对该像素点进行累加
                            continue

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
            ret, thresh = cv2.threshold(gray, 240, 255, 0)  # 二值化
            kernel = np.ones((5, 5), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算
            contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测

            for c in range(len(contours)):
                if cv2.contourArea(contours[c])< threshold:
                    continue
                (cx,cy),(a,b),angle = cv2.fitEllipse(contours[c])#（x, y）代表椭圆中心点的位置
                                                                 #（a, b）代表长短轴长度，应注意a、b为长短轴的直径，而非半径
                                                                 # #angle 代表了中心旋转的角度

                th = 2 * math.pi * angle / 360
                cos = math.cos(th)
                sin = math.sin(th)
                cx=int(cx)
                cy=int(cy)
                a=int(a)
                b=int(b)
                #print(cx,cy,a,b,angle)
                cv2.ellipse(frame,(np.int32(cx),np.int32(cy)),
                            (np.int32(a/2), np.int32(b/2)), angle, 0, 360, (0, 0, 255), 2, 8, 0)
                for i in range(0,size[0]):
                    for j in range(0,size[1]):
                        #print(int(i*cos)+int(j*sin),cx,int(-i*sin)+int(j*cos),cy,a,b)

                        if math.pow((int(i-cx)*cos+int(j-cy)*sin),2)/(a*a)+math.pow((int(j-cy)*cos-int(i-cx)*sin),2)/(b*b)<=0.25:#长轴为x轴，且像素点在方框内
                            data_A[i][j]+=1#若在椭圆内，则对该像素点进行累加
                #frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)#在原图中画轮廓
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

cv2.imshow('grayimage', data_A)
cv2.imwrite('%s.jpg'%input, data_A)
M=np.max(data_A)#均一化
print(M)
data_B=data_A/M
data_C=data_B*255
b = data_C.astype(np.uint8)
color=cv2.applyColorMap(b, cv2.COLORMAP_JET)
cv2.imwrite('%s-%d.jpg'%(input,nihe), color)
cap.release()
out.release()
cv2.destroyAllWindows()

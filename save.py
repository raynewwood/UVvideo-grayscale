import numpy as np
import cv2

cap = cv2.VideoCapture('c01.avi')

# Define the codec and create VideoWriter object

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, size,1)

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        #frame = cv2.flip(frame,0)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#灰度化
        ret, thresh = cv2.threshold(gray, 230, 255, 0)  # 二值化
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)#开运算
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)#闭运算


        contours, hierarchy = cv2.findContours(closing, 3, 1)#轮廓检测
        for c in range(len(contours)):
            (cx,cy),(a,b),angle = cv2.fitEllipse(contours[c])
            cv2.ellipse(frame,(np.int32(cx),np.int32(cy)),
                        (np.int32(a/2), np.int32(b/2)), angle, 0, 360, (0, 0, 255), 2, 8, 0)
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

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

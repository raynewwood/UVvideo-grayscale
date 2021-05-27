# UVvideo-grayscale
Leilei Niu
保存的视频只有6k的解决方案链接
https://blog.csdn.net/time_future/article/details/103376220

解决轮廓检测与保存
https://blog.csdn.net/hjxu2016/article/details/77833336/

开闭运算
https://segmentfault.com/a/1190000015650320

计算重心和椭圆拟合
https://blog.csdn.net/weixin_39644614/article/details/113313084

算法比较 外接不同图像、计算轮廓周长和长度
https://www.cnblogs.com/little-monkey/p/7469354.html
https://blog.csdn.net/yukinoai/article/details/87892718


判断一个点是否在任意矩形之内

1、求4个角点的坐标

https://blog.csdn.net/Maisie_Nan/article/details/105833892  
2、判断

https://blog.csdn.net/taihuoxi6983/article/details/108615695

主要思路为：

将紫外放电视频转换为针对放电点的灰度值图像，并据此对放电性质进行诊断

先决条件：

1、视频中的视场角需要稳定，不能发生较大变化

2、视频内无较大的白色区域

主要步骤

1、视频分帧

2、帧处理（灰度化，二值化，小面积消除，开运算，闭运算）

3、进行轮廓提取

4、进行像素点枚举，判断像素点是否在轮廓内

5、如果在轮廓内则累加

6、选择不同的轮廓类型

7、选择不同的视频时间长度

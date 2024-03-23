"""
摄像头工具
"""

import cv2
from util import public_tools as tool
from util import io_tools as io
from service import recognize_service as rs
from service import hr_service as hr

ESC_KEY = 27  # Esc键的ASCII码
ENTER_KEY = 13  # Enter键的ASCII码


# 打开摄像头进行登记
def register(code):
    cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 获得默认摄像头
    success, frame = cameraCapture.read()  # 读取一帧
    shooting_time = 0  # 拍摄次数
    while success:  # 如果读到有效帧数
        cv2.imshow("register", frame)  # 展示当前画面
        success, frame = cameraCapture.read()  # 再读一帧
        key = cv2.waitKey(1)  # 记录当前用户敲下的按键
        if key == ESC_KEY:  # 如果直接按ESC键
            break  # 停止循环
        if key == ENTER_KEY:  # 如果按Enter键
            # 将当前帧缩放成统一大小
            photo = cv2.resize(frame, (io.IMG_WIDTH, io.IMG_HEIGHT))
            # 拼接照片名：照片文件夹+特征码+随机数字+图片后缀
            img_name = io.PIC_PATH + str(code) + str(tool.randomNumber(8)) + ".png"
            cv2.imwrite(img_name, photo)  # 保存将图像
            shooting_time += 1  # 拍摄次数递增
            if shooting_time == 3:  # 如果拍完三张照片
                break  # 停止循环
    cv2.destroyAllWindows()  # 释放所有窗体
    cameraCapture.release()  # 释放摄像头
    io.load_employee_pic()  # 让人脸识别服务重新载入员工照片


# 打开摄像头打卡
def clock_in():
    cameraCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 获得默认摄像头
    success, frame = cameraCapture.read()  # 读取一帧
    while success and cv2.waitKey(1) == -1:  # 如果读到有效帧数
        cv2.imshow("check in", frame)  # 展示当前画面
        gary = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将彩色图片转为灰度图片
        if rs.found_face(gary):  # 如果屏幕中出现正面人脸
            gary = cv2.resize(gary, (io.IMG_WIDTH, io.IMG_HEIGHT))  # 将当前帧缩放成统一大小
            code = rs.recognise_face(gary)  # 识别图像
            print(code)
            if code != -1:  # 如果识别成功
                print(code)
                name = hr.get_name_with_code(code)  # 获取此特征码对应的员工
                if name != None:  # 如果返回的结果不是空的
                    cv2.destroyAllWindows()  # 释放所有窗体
                    cameraCapture.release()  # 释放摄像头
                    return name  # 返回打卡成功者的姓名
        success, frame = cameraCapture.read()  # 再读一帧
    cv2.destroyAllWindows()  # 释放所有窗体
    cameraCapture.release()  # 释放摄像头

"""
人脸识别服务
"""

import cv2
import numpy as np
import os

RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()  # LBPH识别器
# RECOGNIZER = cv2.face.EigenFaceRecognizer_create()#特征脸识别器
# RECOGNIZER = cv2.face.FisherFaceRecognizer_create()  # LBPH识别器
PASS_CONF = 45  # 最高评分，LBPH最高建议用45，特征脸最高建议用22000
FACE_CASCADE = cv2.CascadeClassifier(os.getcwd() + "\\cascades\\haarcascade_frontalface_default.xml")  # 加载人脸识别级联分类器


# 训练识别器
def train(photos, lables):
    RECOGNIZER.train(photos, np.array(lables))  # 识别器开始训练


# 识别器识别图像中的人脸
def recognise_face(photo):
    label, confidence = RECOGNIZER.predict(photo)  # 识别器开始分析人脸图像
    if confidence > PASS_CONF:  # 忽略评分大于最高评分的结果
        return -1
    return label


# 判断图像中是否有正面人脸
def found_face(gary_img):
    faces = FACE_CASCADE.detectMultiScale(gary_img, 1.15, 4)  # 找出图像中所有的人脸
    return len(faces) > 0  # 返回人脸数量大于0的结果

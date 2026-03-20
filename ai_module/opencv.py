from ultralytics import YOLO
from scipy.spatial import procrustes
import numpy as np
import cv2 as cv
import time

import fay_booter
from core import fay_core
from scheduler.thread_manager import MyThread

__fei_eyes = None


class FeiEyes:

    def __init__(self):

        self.recognizer = cv.face.LBPHFaceRecognizer.create()
        self.recognizer.read(r'D:\Desktop\Fay-fay-assistant-edition\face_recognition\recognizer.yml')
        self.names = []
        # self.warningtime = 0
        self.is_running = False
        self.user_time = 0
        self.user = None
        self.now_user = None

    def face_detector(self, img):
        grey_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        face_detect = cv.CascadeClassifier(r'D:\Desktop\Fay-fay-assistant-edition\face_recognition\haarcascade_frontalface_default.xml')
        face = face_detect.detectMultiScale(grey_img, 1.2, 5)
        if face is not None:
            for (x, y, w, h) in face:
                cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # 人脸识别
                ids, confidence = self.recognizer.predict(grey_img[y:y + h, x:x + w])

                print('标签id：', ids, '置信评分：', confidence)
                if confidence > 150:
                    # self.warningtime += 1
                    cv.putText(img, 'unknown', (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                    cv.imshow('result', img)
                    return 'unknown'
                    # if self.warningtime > 2:
                    #     self.warningtime = 0
                    #     return 'unknown'
                    # cv.putText(img, 'unknown', (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    # cv.imshow('result', img)

                else:
                    cv.putText(img, str(ids), (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                    cv.imshow('result', img)
                    return str(ids)
        cv.imshow('result', img)
        return None


    def get_user(self):
        return self.user


    def get_status(self):
        return self.is_running

    def start(self):
        cap = cv.VideoCapture(0)
        if cap.isOpened():
            self.is_running = True
            MyThread(target=self.run, args=[cap]).start()

    def stop(self):
        self.is_running = False

    def run(self, cap):

        while self.is_running:
            flag, frame = cap.read()
            if not flag:
                break
            self.now_user = self.face_detector(frame)
            if self.user_time == 0 and self.user is not None:
                self.user = None
            elif self.now_user != self.user and self.user_time > 0:
                self.user_time -= 1
            elif self.now_user == self.user and self.user_time > 0 and self.user_time < 120:
                self.user_time += 1
            elif self.now_user != self.user and self.user_time == 0 and self.user is None:
                self.user_time = 100
                self.user = self.now_user
                if fay_booter.feiFei is not None:
                    MyThread(target=fay_booter.feiFei.hello, args=['interact', self.user]).start()
                # print(self.user)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放内存
        cv.destroyAllWindows()

        # 释放摄像头
        cap.release()


def new_instance():
    global __fei_eyes
    if __fei_eyes is None:
        __fei_eyes = FeiEyes()
    return __fei_eyes






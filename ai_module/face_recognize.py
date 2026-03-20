import json
import os
import threading

import face_recognition
from ultralytics import YOLO
from scipy.spatial import procrustes
import numpy as np
import cv2 as cv
import time
import io
import requests

import fay_booter
from core import fay_core
from scheduler.thread_manager import MyThread
from PIL import Image, ImageDraw, ImageFont

__fei_eyes = None


class FeiEyes:

    def __init__(self):

        self.is_running = False
        self.user = None
        self.now_user = None
        self.rtsp_url = None

        self.users = [None, None, None, None, None]
        self.cap = None


    def get_user(self):
        return self.user

    def get_users(self):
        count_dict = {}
        for item in self.users:
            if item in count_dict:
                count_dict[item] += 1
            else:
                count_dict[item] = 1

        max_count = 0
        max_item = None
        for item, count in count_dict.items():
            if count > max_count:
                max_count = count
                max_item = item

        print(max_item)
        return max_item


    def get_status(self):
        return self.is_running

    def start(self):
        self.is_running = True
        MyThread(target=self.run, args=[]).start()
        # cap = cv.VideoCapture(self.rtsp_url)
        # if cap.isOpened():
        #
        #     MyThread(target=self.run, args=[cap]).start()

    def stop(self):
        self.is_running = False

    def adaface(self, frame):
        # 使用BytesIO对象来代替文件
        buffer = io.BytesIO()

        # 将图像写入BytesIO对象
        result, img_encoded = cv.imencode('.png', frame)
        if result:
            buffer.write(img_encoded.tobytes())

        # 将指针移回开始位置
        buffer.seek(0)

        # 发送POST请求
        url = 'http://192.168.3.63:8766/face/picture'  # 替换为实际的URL
        files = {'file': ('upload.png', buffer, 'image/png')}
        response = requests.post(url, files=files)

        response_dict = json.loads(response.text)
        unicode_str = response_dict['final_user']

        # for i in range(0, len(self.users) - 1):
        #     self.users[i] = self.users[i+1]
        # self.users[len(self.users)-1] = unicode_str
        #
        # print(str(self.users))

        # if fay_booter.feiFei is not None:
        #     if self.user != self.get_users():
        #         self.user = self.get_users()
        #         print(self.user)
        #         MyThread(target=fay_booter.feiFei.hello, args=['interact', self.user]).start()

        if fay_booter.feiFei is not None:
            if self.user != unicode_str:
                self.user = unicode_str
                print(self.user)
                MyThread(target=fay_booter.feiFei.hello, args=['interact', self.user]).start()

    def run(self):

        self.cap = cv.VideoCapture(self.rtsp_url)
        ret_num = 0

        while self.is_running:
            if not self.cap.isOpened():
                self.cap = cv.VideoCapture(self.rtsp_url)
            ret, frame = self.cap.read()
            # print(self.user)
            if not ret:
                break

            ret_num += 1
            # if ret_num % 30 == 0:
            #     thread = threading.Thread(target=lambda: self.adaface(frame))
            #     thread.start()
            cv.imshow("video",frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放内存
        cv.destroyAllWindows()

        # 释放摄像头
        self.cap.release()


def new_instance():
    global __fei_eyes
    if __fei_eyes is None:
        __fei_eyes = FeiEyes()
    return __fei_eyes






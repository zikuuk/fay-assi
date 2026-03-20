import os
import sys
from io import BytesIO

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from ai_module import ali_nls
from ai_module import nlp_langchain
from core import wsa_server
from gui import flask_server
from gui.window import MainWindow
from utils import config_util
from scheduler.thread_manager import MyThread
from core import content_db
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)
import hashlib
import os
import time




# from multiprocessing import Process
#
# def run_script():
#     import sys
#     from subprocess import call
#     call(['python', './logfile/client.py'])





def __clear_samples():
    if not os.path.exists("./samples"):
        os.mkdir("./samples")
    for file_name in os.listdir('./samples'):
        if file_name.startswith('sample-'):
            os.remove('./samples/' + file_name)


def __clear_songs():
    if not os.path.exists("./songs"):
        os.mkdir("./songs")
    for file_name in os.listdir('./songs'):
        if file_name.endswith('.mp3'):
            os.remove('./songs/' + file_name)

def __clear_logs():
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    for file_name in os.listdir('./logs'):
        if file_name.endswith('.log'):
            os.remove('./logs/' + file_name)
           


if __name__ == '__main__':

    # # 创建一个新的进程来运行脚本
    # process = Process(target=run_script)
    # process.start()

    __clear_samples() # 清理
    __clear_songs()
    __clear_logs()
    config_util.load_config() #加载配置
    contentdb = content_db.new_instance() #实例化数据库类
    contentdb.init_db()     #数据库初始化
    ws_server = wsa_server.new_instance(port=10002)  #实例化数字人server
    ws_server.start_server()  #启动数字人server
    web_ws_server = wsa_server.new_web_instance(port=10003)
    web_ws_server.start_server()
    #Edit by xszyou in 20230516:增加本地asr后，aliyun调成可选配置
    if config_util.ASR_mode == "ali":
        ali_nls.start()     #启动阿里自动语音识别
    flask_server.start() 
    if config_util.key_chat_module == 'langchain':
        nlp_langchain.save_all()

    #  创建一个QApplication实例，这是PyQt应用程序的中心类。sys.argv是一个列表，包含了从命令行传递给Python脚本的参数。QApplication初始化图形用户界面应用程序，并处理这些命令行参数。
    app = QApplication(sys.argv)

    #图标
    app.setWindowIcon(QtGui.QIcon('icon.png'))

    #创建一个MainWindow类的实例。MainWindow类很可能是应用程序的主窗口或主界面。
    win = MainWindow()
    time.sleep(1)
    win.show()    # 显示MainWindow窗口

    # 启动应用程序的事件循环。调用QApplication对象的exec_()方法，该方法启动事件循环并处理用户界面。当事件循环退出时，QApplication对象的exit()方法被调用，并传递一个退出代码0，表示应用程序已成功完成。
    app.exit(app.exec_())

    

import sys
import threading

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from TCP_client import *
from model_user import User
from view_friend_list import ViewFriendList
from view_widget import Widget
from multiprocessing import Process

class Ui_ViewMain(Widget):
    """
    登录后的主界面
    """
    flush_msg = pyqtSignal(object)
    recv_chat_msg = pyqtSignal(object)
    recv_chat_img = pyqtSignal(object)

    def __init__(self, account,sockfd):
        super().__init__()
        self.user = User()
        self.sockfd =sockfd
        self.user = find_all_info_by_account(account)
        self.friend_list = find_all_friends(account)
        self.setupUi()

    def setupUi(self):
        # 设置主窗口
        self.setObjectName("ViewMain")
        self.resize(288, 658)
        self.setStyleSheet("")

        # 好友和群聊按钮区
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 140, 288, 42))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                 "border:none")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # 选择好友界面的按钮
        self.pushButton_friends = QtWidgets.QPushButton(self.frame)
        self.pushButton_friends.setGeometry(QtCore.QRect(5, 9, 121, 21))
        self.pushButton_friends.setObjectName("pushButton_friends")
        self.pushButton_friends.clicked.connect(self.show_friend)
        # 选择群聊界面的按钮
        self.pushButton_group = QtWidgets.QPushButton(self.frame)
        self.pushButton_group.setGeometry(QtCore.QRect(159, 9, 121, 21))
        self.pushButton_group.setObjectName("pushButton_group")
        self.pushButton_group.clicked.connect(self.show_group)
        # 选中好友后显示的蓝标
        self.label_friend_show = QtWidgets.QLabel(self.frame)
        self.label_friend_show.setGeometry(QtCore.QRect(40, 40, 67, 2))
        self.label_friend_show.setStyleSheet("background-color: rgb(57, 99, 255);")
        self.label_friend_show.setText("")
        self.label_friend_show.setObjectName("label_friend_show")
        # 选中群聊后显示的蓝标
        self.label_group_show = QtWidgets.QLabel(self.frame)
        self.label_group_show.setGeometry(QtCore.QRect(185, 40, 67, 2))
        self.label_group_show.setStyleSheet("background-color: rgb(57, 99, 255);")
        self.label_group_show.setText("")
        self.label_group_show.setObjectName("label_group_show")
        self.label_group_show.hide()
        # 上部分区域
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 288, 140))
        self.frame_2.setStyleSheet("background-image: url(res/main/背景1.png);\n"
                                   "border:none")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        # 头像按钮
        self.pushButton_head = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_head.setGeometry(QtCore.QRect(10, 31, 50, 50))

        self.pushButton_head.setText("")
        self.pushButton_head.setObjectName("pushButton_head")
        if self.user.img == None:
            self.user.img = "椭圆 1 拷贝.png"
        filepath = "res/client_head_image/%s" % self.user.img
        is_exist = os.path.exists(filepath)
        if is_exist == False:
            download_head_img_by_account(self.user.img)
            self.pushButton_head.setStyleSheet("border-image: url(res/client_head_image/%s);"% self.user.img)
        else:
            self.pushButton_head.setStyleSheet("border-image: url(res/client_head_image/%s);" % self.user.img)
        # 昵称文字
        self.label_nickname = QtWidgets.QLabel(self.frame_2)
        self.label_nickname.setGeometry(QtCore.QRect(70, 35, 131, 20))
        self.label_nickname.setStyleSheet("color: rgb(255, 255, 255);background:transparent")
        self.label_nickname.setObjectName("label_nickname")
        # 邮箱文字
        self.label_email = QtWidgets.QLabel(self.frame_2)
        self.label_email.setGeometry(QtCore.QRect(70, 65, 140, 13))
        self.label_email.setStyleSheet("color: rgb(255, 255, 255);font: 8pt \"Ubuntu\";background:transparent")
        self.label_email.setObjectName("label_email")
        # 关闭按钮
        self.pushButton_exit = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_exit.setGeometry(QtCore.QRect(254, 0, 34, 34))
        self.pushButton_exit.setStyleSheet("background-image: url(res/main/组 8.png);")
        self.pushButton_exit.setText("")
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.pushButton_exit.clicked.connect(self.close_view)
        # 最小化按钮
        self.pushButton_min = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_min.setGeometry(QtCore.QRect(220, 0, 34, 34))
        self.pushButton_min.setStyleSheet("background-image: url(res/main/组 9.png);")
        self.pushButton_min.setText("")
        self.pushButton_min.setObjectName("pushButton_min")
        self.pushButton_min.clicked.connect(self.showMinimized)
        # 搜索区域
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        self.frame_3.setGeometry(QtCore.QRect(10, 96, 228, 28))
        self.frame_3.setStyleSheet("")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        # 搜索框
        self.lineEdit_search = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_search.setGeometry(QtCore.QRect(28, 0, 200, 28))
        self.lineEdit_search.setStyleSheet("color: rgb(255, 255, 255);font: 8pt \"Ubuntu\";background:transparent")
        self.lineEdit_search.setObjectName("lineEdit_search")
        # 搜索图标
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(6, 5, 16, 16))
        self.label_3.setStyleSheet("background-image: url(res/main/形状 2.png);")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        # 添加按钮
        self.pushButton_add = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_add.setGeometry(QtCore.QRect(248, 95, 30, 30))
        self.pushButton_add.setStyleSheet("background-image: url(res/main/按钮.png);")
        self.pushButton_add.setText("")
        self.pushButton_add.setObjectName("pushButton_add")

        # 天气显示
        self.label_weather = QtWidgets.QLabel(self.frame_2)
        self.label_weather.setGeometry(QtCore.QRect(240, 40, 32, 20))
        self.label_weather.setStyleSheet("color: rgb(255, 255, 255);font: 8pt \"Ubuntu\";background:transparent")
        self.label_weather.setObjectName("label_weather")
        # 温度显示
        self.label_temperature = QtWidgets.QLabel(self.frame_2)
        self.label_temperature.setGeometry(QtCore.QRect(240, 60, 41, 20))
        self.label_temperature.setStyleSheet("color: rgb(255, 255, 255);font: 8pt \"Ubuntu\";background:transparent")
        self.label_temperature.setObjectName("label_temperature")
        # 底部区域 好友列表
        self.frame_4 = QtWidgets.QFrame(self)
        self.frame_4.setGeometry(QtCore.QRect(0, 182, 288, 476))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.friends = ViewFriendList(self.frame_4, self.user,self.friend_list)
        self.frame_4.show()
        # 群聊区域
        self.frame_5 = QtWidgets.QFrame(self)
        self.frame_5.setGeometry(QtCore.QRect(0, 182, 288, 476))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_4")
        # self.group = ViewGroupList(self.frame_5)
        self.frame_5.hide()

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # 绑定信号
        self.flush_msg.connect(self.friends.singla_flush)
        self.recv_chat_msg.connect(self.friends.singla_recv_chat_message)
        self.recv_chat_img.connect(self.friends.singla_recv_chat_image)

        self.thread = threading.Thread(target=self.recv_message)
        self.thread.setDaemon(True)
        self.thread.start()
        # self.process = Process(target=self.recv_message)
        # self.process.daemon = True
        # self.process.start()

    def recv_message(self):
        print("开始了接收消息的子进程")
        while True:
            try:
                data = self.sockfd.recv(1024).decode()
            except Exception as e:
                print(e)
            list_data = data.split(" ", 1)
            if list_data[0] == "FRIEND_ONLINE":
                self.do_friend_online(list_data)
                # account = list_data[1]
                # message = "FIND_ALL_FRIENDS %s" % self.user.account_id
                # try:
                #     self.sockfd.send(message.encode())  # 发送字节串
                # except:
                #     return "CONNECT_FAILED"
                # try:
                #     msg_json = sockfd.recv(1024 * 1204)
                #     list_friend_account = json.loads(msg_json.decode())
                #     list_friends = []
                #     if list_friend_account == False:
                #         return list_friends
                #     else:
                #         for account in list_friend_account:
                #             user = find_all_info_by_account(account)
                #             list_friends.append(user)
                #     self.friend_list = list_friends
                # except:
                #     print("好友上线获取失败")
                # self.flush_friend_list()
            elif list_data[0]== "CHAT":    # list_data = ['CHAT', 'admin admin1 李行 2019-12-02-13:09:28: 111111']
                self.do_chat(list_data)
            elif list_data[0]=="SEND_CHAT_IMG": # list_data = ['SEND_CHAT_IMG', 'filesize file_name recv_account send_account']
                data = self.do_send_chat_img(data, list_data)

    def do_friend_online(self,list_data):
        account = list_data[1]
        message = "FIND_ALL_FRIENDS %s" % self.user.account_id
        try:
            self.sockfd.send(message.encode())  # 发送字节串
        except:
            return "CONNECT_FAILED"
        try:
            msg_json = sockfd.recv(1024 * 1204)
            list_friend_account = json.loads(msg_json.decode())
            list_friends = []
            if list_friend_account == False:
                return list_friends
            else:
                for account in list_friend_account:
                    user = find_all_info_by_account(account)
                    list_friends.append(user)
            self.friend_list = list_friends
        except:
            print("好友上线获取失败")
        self.flush_friend_list()

    def do_send_chat_img(self, data, list_data):
        temp = list_data[1].split(" ", 3)
        filesize = temp[0]
        filename = temp[1]
        recv_account = temp[2]
        send_account = temp[3]
        filepath = "res/chat_img_client/%s" % filename
        fw = open(filepath, "wb")
        file_total_size = int(filesize)
        receive_size = 0
        while receive_size < file_total_size:
            data = sockfd.recv(1024)
            receive_size += len(data)
            fw.write(data)
            fw.flush()
        fw.close()
        message = "%s %s" % (send_account, filepath)
        self.recv_chat_img.emit(message)
        return data

    def do_chat(self, list_data):
        chat_message = list_data[1]  # chat_message='admin admin1 李行 2019-12-02-13:09:28: 111111'
        self.recv_chat_message(chat_message)

    def recv_chat_image(self,msg):
        self.recv_chat_img.emit(msg)

    def flush_friend_list(self):
        message = "FLUSH "
        json_list_friend = []
        for friend in self.friend_list:
            dict_friend = friend.__dict__
            json_friend = json.dumps(dict_friend)
            json_list_friend.append(json_friend)
        json_list_friend = json.dumps(json_list_friend)
        message += json_list_friend
        # 发射信号
        self.flush_msg.emit(message)

    def recv_chat_message(self,msg): #msg = '彭琦 2019-12-02-12:35:53: 11111'
        self.recv_chat_msg.emit(msg)

    def close_view(self):
        exit(self.user.account_id)
        self.close()

    def flush_friends_list(self):
        self.friends.flush_friend_list()

    def show_group(self):
        self.label_friend_show.hide()
        self.label_group_show.show()
        self.frame_4.hide()
        self.frame_5.show()

    def show_friend(self):
        self.label_group_show.hide()
        self.label_friend_show.show()
        self.frame_5.hide()
        self.frame_4.show()

    def open_self(self):
        self.show()

    def retranslateUi(self, ViewMain):
        _translate = QtCore.QCoreApplication.translate
        ViewMain.setWindowTitle(_translate("ViewMain", "Form"))
        self.pushButton_friends.setText(_translate("ViewMain", "     好 友"))
        self.pushButton_group.setText(_translate("ViewMain", "群 组"))
        self.label_nickname.setText(_translate("ViewMain", "%s" % self.user.nickname))
        # self.label_email.setText(_translate("ViewMain", "邮箱:545686004@qq.com"))
        self.lineEdit_search.setPlaceholderText(_translate("ViewMain", "搜索"))
        self.label_weather.setText(_translate("ViewMain", "多云"))
        self.label_temperature.setText(_translate("ViewMain", "2-8度"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sockfd = connect_server()
    login = Ui_ViewMain("admin",sockfd)
    login.show()
    sys.exit(app.exec_())
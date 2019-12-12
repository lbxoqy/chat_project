import os
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from TCP_client import download_head_img_by_account, find_all_info_by_account, connect_server
from view.view_chat import Ui_ViewChat


class Ui_ViewFriendItem(QWidget):
    """
    好友单个item窗口
    """
    flush_msg = pyqtSignal(object)
    flush_chat_img = pyqtSignal(object)

    def __init__(self,user, user_friend):
        super(Ui_ViewFriendItem, self).__init__()
        self.user = user
        self.user_friend = user_friend
        self.friend_message = []
        self.img_path = ""
        self.setupUi()

    def setupUi(self):
        self.setObjectName("ViewFriendItem")
        self.resize(288, 70)
        # 头像框
        self.label_head_img = QtWidgets.QPushButton(self)
        self.label_head_img.setGeometry(QtCore.QRect(10, 15, 40, 40))
        if self.user_friend.img == None or self.user_friend.img == "":
            self.label_head_img.setStyleSheet("border-image: url(res/client_head_image/logo.png);")
        else:
            is_exist = os.path.exists("res/client_head_image/%s" % self.user_friend.img)
            if is_exist == True:
                pass
            else:
                download_head_img_by_account(self.user_friend.img)
            self.label_head_img.setStyleSheet("border-image: url(res/client_head_image/%s);" % self.user_friend.img)
        self.label_head_img.setText("")
        self.label_head_img.setObjectName("label_head_img")
        # 昵称框
        self.label_nickname = QtWidgets.QLabel(self)
        self.label_nickname.setGeometry(QtCore.QRect(60, 18, 211, 17))
        self.label_nickname.setObjectName("label_nickname")
        # 设置消息提醒动图
        self.gif = QMovie("res/main/红点.gif")
        self.lable_message = QLabel(self)
        self.lable_message.setGeometry(40, 13, 20, 20)
        self.lable_message.setMovie(self.gif)
        self.gif.start()
        self.lable_message.hide()
        # 在线图标
        self.label_online_img = QtWidgets.QLabel(self)
        self.label_online_img.setGeometry(QtCore.QRect(60, 40, 16, 16))
        if self.user_friend.online_status == 1:
            self.label_online_img.setStyleSheet("border-image: url(res/main/形状 3.png);")
        else:
            self.label_online_img.setStyleSheet("border-image: url(res/main/形状 5.png);")
        self.label_online_img.setText("")
        self.label_online_img.setObjectName("label_online_img")
        # 在线文字
        self.label_online = QtWidgets.QLabel(self)
        self.label_online.setGeometry(QtCore.QRect(80, 40, 25, 13))
        if self.user_friend.online_status == True:
            self.label_online.setStyleSheet("font: 9pt \"Ubuntu\";\n"
                                            "color: rgb(71, 185, 116);")
        else:
            self.label_online.setStyleSheet("font: 9pt \"Ubuntu\";\n"
                                            "color: #999999;")
        self.label_online.setObjectName("label_online")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def mouseDoubleClickEvent(self, QMouseEvent):
        self.view_chat = Ui_ViewChat(self.user,self.user_friend)
        self.lable_message.hide()
        self.view_chat.show()
        self.view_chat.friend_message = self.friend_message
        self.view_chat.img_path = self.img_path
        #     绑定信号
        self.flush_msg.connect(self.view_chat.singla_flush_chat)
        self.flush_chat_img.connect(self.view_chat.singla_flush_img)
        self.recv_chat_message("FLUSH_CHAT")
        self.recv_chat_image("FLUSH_CHAT_IMG %s"%self.img_path)


    def recv_chat_image(self,msg):
        self.flush_chat_img.emit(msg)

    def recv_chat_message(self, msg):
        self.flush_msg.emit(msg)

    def retranslateUi(self, ViewFriendItem):
        _translate = QtCore.QCoreApplication.translate
        ViewFriendItem.setWindowTitle(_translate("ViewFriendItem", "Form"))
        if self.user_friend.offline_message == False:
            self.label_nickname.setText(_translate("ViewFriendItem", "%s" % self.user_friend.nickname))
        else:
            self.label_nickname.setText(_translate("ViewFriendItem", "%s 有消息来啦" % self.user_friend.nickname))
        if self.user_friend.online_status == True:
            self.label_online.setText(_translate("ViewFriendItem", "在线"))
        else:
            self.label_online.setText(_translate("ViewFriendItem", "离线"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sockfd = connect_server()
    user = find_all_info_by_account("admin")
    print(user.img)
    friend = find_all_info_by_account("admin1")
    print(friend.img)
    login = Ui_ViewFriendItem(user,friend)
    login.show()
    sys.exit(app.exec_())

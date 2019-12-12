# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_chat.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!
import sys
import time

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *

from TCP_client import send_chat, find_all_friends, send_img
from view_widget import Widget
from model_user import User


class Ui_ViewChat(Widget):

    def __init__(self,user, user_friend):
        super().__init__()
        self.user = user
        self.user_friend = user_friend
        self.friend_message = []
        self.img_path = ""
        self.setupUi()
    def setupUi(self):
        self.setObjectName("Form")
        self.resize(800, 632)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 0, 800, 65))
        self.frame.setStyleSheet("border:none;background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        # 关闭按钮
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(766, 0, 34, 22))
        self.pushButton.setStyleSheet("background-image: url(res/chat/关闭.png);border:none;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close)
        # 最小化按钮
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(732, 0, 34, 22))
        self.pushButton_2.setStyleSheet("background-image: url(res/chat/最小化.png);border:none;")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.showMinimized)
        # 头像按钮
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 7, 50, 50))
        if self.user_friend.img == None or self.user_friend.img =="":
            self.user_friend.img = "logo.png"
        self.pushButton_3.setStyleSheet("border-image: url(res/client_head_image/%s);"%self.user_friend.img)
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        # 对方昵称
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(80, 13, 271, 30))
        self.label.setStyleSheet("font: 18pt \"Ubuntu\";")
        self.label.setObjectName("label")
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(0, 65, 800, 420))
        self.frame_2.setStyleSheet("border:none;background-color: rgb(255, 255, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.listWidget = QtWidgets.QListWidget(self.frame_2)
        self.listWidget.setGeometry(QtCore.QRect(5, 0, 790, 420))
        self.listWidget.setStyleSheet("background-color: rgb(242, 243, 243);")
        self.listWidget.setObjectName("listWidget")
        # 去除滚动条
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.frame_2.show()

        self.frame_3 = QtWidgets.QFrame(self)
        self.frame_3.setGeometry(QtCore.QRect(0, 485, 800, 147))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_4 = QtWidgets.QFrame(self.frame_3)
        self.frame_4.setGeometry(QtCore.QRect(3, 0, 796, 42))
        self.frame_4.setStyleSheet("background-color: rgb(255, 255, 255);border:none;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_4.setGeometry(QtCore.QRect(16, 10, 24, 22))
        self.pushButton_4.setStyleSheet("background-image: url(res/chat/表情.png);border:none;")
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.send_expression)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_5.setGeometry(QtCore.QRect(51, 10, 24, 22))
        self.pushButton_5.setStyleSheet("background-image: url(res/chat/图片.png);border:none;")
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.send_img)
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_6.setGeometry(QtCore.QRect(86, 10, 24, 22))
        self.pushButton_6.setStyleSheet("border:none;background-image: url(res/chat/文件.png);")
        self.pushButton_6.setText("")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.send_file)
        self.pushButton_7 = QtWidgets.QPushButton(self.frame_4)
        self.pushButton_7.setGeometry(QtCore.QRect(760, 10, 24, 22))
        self.pushButton_7.setStyleSheet("border:none;background-image: url(res/chat/历史记录.png);")
        self.pushButton_7.setText("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.show_history)
        self.textEdit = QtWidgets.QTextEdit(self.frame_3)
        self.textEdit.setGeometry(QtCore.QRect(5, 42, 700, 105))
        self.textEdit.setStyleSheet("border:none;background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        self.pushButton_8 = QtWidgets.QPushButton(self.frame_3)
        self.pushButton_8.setGeometry(QtCore.QRect(705, 42, 95, 105))
        self.pushButton_8.setStyleSheet("border:none;font: 57 italic 11pt \"Ubuntu\";font: 20pt \"Ubuntu\";background-color: rgb(242, 243, 243);")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.send_chat)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.flush_message_list()

    def singla_flush_chat(self, msg):
        if msg == "FLUSH_CHAT":
            self.flush_message_list()

    def flush_message_list(self):
        for text in self.friend_message: # text = '彭琦 2019-12-02-13:31:27: 11111'
            list_text = text.split(" ", 2)
            nickname = list_text[0]
            time = list_text[1]
            msg = list_text[2]
            item = QListWidgetItem()
            item.setSizeHint(QSize(288, 34))
            label = QtWidgets.QLabel()
            label.setText("%s %s:" % (nickname, time))
            label.setStyleSheet("color: rgb(245, 121, 0);")
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, label)
            item = QListWidgetItem()
            item.setSizeHint(QSize(288, 34))
            label2 = QtWidgets.QLabel()
            label2.setText("%s" % msg)
            label2.setStyleSheet("font: 15pt ;")
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, label2)
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.friend_message.clear()
        QApplication.processEvents()

    def singla_flush_img(self,msg):  # msg = "FLUSH_CHAT_IMG res/chat_img_client/admin2.jpg"
        print(msg)
        temp = msg.split(" ",1)
        result = temp[0]
        filepath = temp[1]
        if result == "FLUSH_CHAT_IMG":
            self.flush_chat_image(filepath)

    def flush_chat_image(self,filepath):
        if filepath == "":
            pass
        else:
            current_time_tuple = time.localtime()
            current_time_str = time.strftime("%Y-%m-%d-%H:%M:%S", current_time_tuple)
            item = QListWidgetItem()
            item.setSizeHint(QSize(288, 34))
            label = QtWidgets.QLabel()
            label.setText("%s %s:" % (self.user.nickname, current_time_str))
            label.setStyleSheet("color: rgb(245, 121, 0);")
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, label)
            try:
                if filepath.split(".")[-1]=="gif":
                    img = Image.open(filepath)
                    imgSize = img.size  # 图片的长和宽
                    x = imgSize[0] // 2
                    y = imgSize[1] // 2
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(x, y))
                    widget = QWidget()
                    label = QtWidgets.QLabel(widget)
                    label.setGeometry(0, 0, x, y)
                    gif = QMovie(filepath)
                    gif.setScaledSize(QSize(100,100))
                    label.setMovie(gif)
                    gif.start()
                else:
                    img = Image.open(filepath)
                    imgSize = img.size  # 图片的长和宽
                    while True:
                        x = imgSize[0] // 2
                        y = imgSize[1] // 2
                        imgSize = (x, y)
                        if y < 200:
                            break
                    item = QListWidgetItem()
                    item.setSizeHint(QSize(x, y))
                    widget = QWidget()
                    label = QtWidgets.QLabel(widget)
                    label.setGeometry(0, 0, x, y)
                    label.setStyleSheet("border-image: url(%s);" % filepath)
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, widget)
                self.listWidget.setCurrentRow(self.listWidget.count() - 1)
            except:
                print("图片打开失败")

    def send_expression(self):
        pass
    def send_img(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取文件",
                                                                "/home/tarena/",  # 起始路径
                                                                "All Files(*.jpg *.gif *.jpeg)")  # 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            print("\n取消选择")
            return
        self.textEdit.setText('<img src=\"%s\" width="50" />' % fileName_choose)
        self.img_path = fileName_choose

    def send_file(self):
        pass
    def send_chat(self):
        if self.img_path =="":
            current_time_tuple = time.localtime()
            current_time_str = time.strftime("%Y-%m-%d-%H:%M:%S", current_time_tuple)
            text = self.textEdit.toPlainText()
            self.add_chat_item(text,current_time_str)
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)
            self.textEdit.clear()
            message = "%s %s: %s"%(self.user.nickname,current_time_str,text)
            send_chat(self.user.account_id,self.user_friend.account_id,message)
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        else:
            current_time_tuple = time.localtime()
            current_time_str = time.strftime("%Y-%m-%d-%H:%M:%S", current_time_tuple)
            item = QListWidgetItem()
            item.setSizeHint(QSize(288, 34))
            label = QtWidgets.QLabel()
            label.setText("%s %s:" % (self.user.nickname, current_time_str))
            label.setStyleSheet("color: rgb(245, 121, 0);")
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, label)
            if self.img_path.split(".")[-1]=="gif":
                img = Image.open(self.img_path)
                imgSize = img.size  # 图片的长和宽
                x = imgSize[0] // 2
                y = imgSize[1] // 2


                item = QListWidgetItem()
                item.setSizeHint(QSize(x, y))
                widget = QWidget()
                label = QtWidgets.QLabel(widget)
                label.setGeometry(0, 0, x, y)
                gif = QMovie(self.img_path)
                gif.setScaledSize(QSize(100, 100))
                label.setMovie(gif)
                gif.start()
            else:

                img = Image.open(self.img_path)
                imgSize = img.size  # 图片的长和宽
                while True:
                    x = imgSize[0]//2
                    y = imgSize[1]//2
                    imgSize = (x,y)
                    if y < 200:
                        break
                item = QListWidgetItem()
                item.setSizeHint(QSize(x, y))
                widget = QWidget()
                label = QtWidgets.QLabel(widget)
                label.setGeometry(0, 0, x,y)
                label.setStyleSheet("border-image: url(%s);" % self.img_path)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)
            send_img(self.user.account_id,self.user_friend.account_id,self.img_path)
            self.img_path = ""
            self.textEdit.clear()
            self.listWidget.setCurrentRow(self.listWidget.count() - 1)
    def show_history(self):
        pass

    def add_chat_item(self,text,time):
        item = QListWidgetItem()
        item.setSizeHint(QSize(288, 34))
        label = QtWidgets.QLabel()
        label.setText("%s %s:"%(self.user.nickname,time))
        label.setStyleSheet("color: rgb(245, 121, 0);")
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, label)
        item = QListWidgetItem()
        item.setSizeHint(QSize(288, 34))
        label2 = QtWidgets.QLabel()
        label2.setText("%s"%text)
        label2.setStyleSheet("font: 15pt ;")
        self.listWidget.addItem(item)
        self.listWidget.setItemWidget(item, label2)
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "%s"%self.user_friend.nickname))
        self.pushButton_8.setText(_translate("Form", "发\n送"))

    def keyPressEvent(self, event):
        if event.key() == 16777220 or event.key() == 16777221:
            self.send_chat()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    user = User()
    friend = User()
    login = Ui_ViewChat(user,friend)
    login.show()
    sys.exit(app.exec_())

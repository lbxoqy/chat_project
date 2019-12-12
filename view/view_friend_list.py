import json
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *

from TCP_client import connect_server, find_all_info_by_account
from model_user import User
from view.view_friend_item import Ui_ViewFriendItem


class ViewFriendList(QWidget):
    """
    好友列表界面
    """
    def __init__(self, w, user,friend_list):
        super().__init__()
        self.w = w
        self.user = user
        self.friend_list =friend_list
        self.friend_item_dict = {}
        self.setupUi(self.w)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(288, 476)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 288, 476))
        self.listWidget.setObjectName("listWidget")
        # 去除滚动条
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        for friend in self.friend_list:
            widget = Ui_ViewFriendItem(self.user, friend)
            self.friend_item_dict[friend.account_id] = widget

        for friend_account,widget in self.friend_item_dict.items():
            item = QListWidgetItem()
            item.setSizeHint(QSize(288, 70))
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

    def singla_recv_chat_image(self,msg):  # msg = "recv_account filepath"
        msg_list = msg.split(" ", 1)
        recv_account = msg_list[0]
        file_path = msg_list[1]
        for friend_account, widget in self.friend_item_dict.items():
            if recv_account == friend_account:
                widget.lable_message.show()
                widget.img_path = file_path
                widget.recv_chat_image("FLUSH_CHAT_IMG %s"%file_path)

    def singla_recv_chat_message(self,msg):  # msg='admin admin1 李行 2019-12-02-13:09:28: 111111'
        msg_list = msg.split(" ",2)
        recv_account = msg_list[0]
        chat_message = msg_list[2]
        for friend_account, widget in self.friend_item_dict.items():
            if recv_account == friend_account:
                widget.lable_message.show()
                widget.friend_message.append(chat_message)
                widget.recv_chat_message("FLUSH_CHAT")

    def singla_flush(self, msg):
        data_list = msg.split(" ",1)
        friend_list = []
        if data_list[0] == "FLUSH":
            json_friend_list  = data_list[1]
            list_json_friend = json.loads(json_friend_list)
            for json_friend in list_json_friend:
                dict_friend = json.loads(json_friend)
                user = User()
                user.__dict__ = dict_friend
                friend_list.append(user)
            self.flush_friend_list(friend_list)

    def flush_friend_list(self,friend_list):
        for i in range(len(self.friend_list)):
            self.listWidget.takeItem(0)
        self.friend_list.clear()
        self.friend_item_dict.clear()
        self.friend_list = friend_list
        for friend in self.friend_list:
            widget = Ui_ViewFriendItem(self.user, friend)
            self.friend_item_dict[friend.account_id] = widget
        for friend_account,widget in self.friend_item_dict.items():
            item = QListWidgetItem()
            item.setSizeHint(QSize(288, 70))
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, widget)
        QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sockfd = connect_server()
    user = find_all_info_by_account("admin")
    w = QWidget()
    login = ViewFriendList(w,user)
    w.show()
    sys.exit(app.exec_())
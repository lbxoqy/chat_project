"""
登录界面
"""
import sys
import webbrowser
from multiprocessing import Process

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel, QDesktopWidget, QApplication, QWidget

from TCP_client import *
from tools_pyqt import *
# from view_main import Ui_ViewMain
from view_main import Ui_ViewMain
from view_widget import Widget


class ViewLogin(Widget):

    def __init__(self,sockfd):
        super().__init__()
        self.sockfd =sockfd
        self.initUI()

    def initUI(self):
        # 登录失败提示
        self.login_failed = QLabel("登录失败...", self)
        self.login_failed.setGeometry(451, 246, 70, 14)
        self.login_failed.setStyleSheet('font-size:12px;''color:red')
        self.login_failed.setHidden(True)
        # 设置右上角X
        self.close_button = QPushButton(self)
        self.close_button.setStyleSheet(
            "QPushButton{background-image: url(res/login/关闭悬浮.png)} QPushButton{border:none;}")
        self.close_button.setGeometry(616, 0, 34, 34)
        self.close_button.pressed.connect(self.close)
        # 设置最小化窗口
        self.min_button = QPushButton(self)
        self.min_button.setStyleSheet(
            "QPushButton{background-image: url(res/login/最小化悬浮.png)} QPushButton{border:none;}")
        self.min_button.setGeometry(582, 0, 34, 34)
        self.min_button.pressed.connect(self.showMinimized)
        # 设置头像动图
        self.gif = QMovie("res/login/dongtu.gif")
        self.lable = QLabel(self)
        self.lable.setGeometry(444, 46, 88, 88)
        self.lable.setMovie(self.gif)
        self.gif.start()
        # 设置用户名图标
        self.user_name_botton = PyqtTools.set_button(self, "res/login/用户名.png", 16, 16, 360, 166)
        self.passwd_botton = PyqtTools.set_button(self, "res/login/密码.png", 16, 16, 359, 210)
        # 设置用户名输入框
        self.account_edit = PyqtTools.set_LineEdit(self, 241, 32, 382, 158, "background-color:#F5F5F5;")
        self.account_edit.setPlaceholderText("请输入账号")
        self.account_edit.textChanged.connect(lambda: self.login_failed.setHidden(True))
        # 设置密码输入矿
        self.passwd_edit = PyqtTools.set_LineEdit(self, 241, 32, 382, 200, "background-color:#F5F5F5;")
        self.passwd_edit.setEchoMode(QLineEdit.Password)
        self.passwd_edit.setPlaceholderText("请输入密码")
        self.passwd_edit.textChanged.connect(lambda: self.login_failed.setHidden(True))
        # 设置登陆按钮
        self.login_button = QPushButton(self)
        self.login_button.setStyleSheet(
            "QPushButton{background-image: url(res/login/登陆.png)} QPushButton{border:none;}")
        self.login_button.setGeometry(353, 271, 270, 34)
        self.login_button.clicked.connect(self.login)
        # 设置注册账号按钮
        self.register_button = QPushButton(self)
        self.register_button.setStyleSheet(
            "QPushButton{background-image: url(res/login/注册账号.png)} QPushButton{border:none;}")
        self.register_button.setGeometry(351, 246, 50, 14)
        self.register_button.clicked.connect(self.register)
        # 设置找回密码按钮
        self.retrieve_passwd = QPushButton(self)
        self.retrieve_passwd.setStyleSheet(
            "QPushButton{background-image: url(res/login/找回密码.png)} QPushButton{border:none;}")
        self.retrieve_passwd.setGeometry(575, 246, 50, 14)
        self.retrieve_passwd.clicked.connect(self.retrieve)
        # 设置左边蓝色框
        self.left_button = QLabel(self)
        self.left_button.setStyleSheet(
            "background-image: url(res/login/矩形 1 拷贝.png)")
        self.left_button.setGeometry(0, 0, 325, 350)

        # 设置按钮的事件
        self.close_button.setMouseTracking(True)
        self.close_button.installEventFilter(self)
        self.min_button.setMouseTracking(True)
        self.min_button.installEventFilter(self)
        self.login_button.setMouseTracking(True)
        self.login_button.installEventFilter(self)

        # 设置主窗口
        PyqtTools.set_background(self, "res/login/右边白色.png")
        self.center()
        self.resize(650, 350)
        self.setWindowTitle("hahah")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon("res/login/xzmly.jpeg"))


    def center(self):
        self.qr = self.frameGeometry()
        self.cp = QDesktopWidget().availableGeometry().center()
        self.qr.moveCenter(self.cp)
        self.move(self.qr.topLeft())


    def login(self):
        account = self.account_edit.text()
        passwd = self.passwd_edit.text()
        re = do_login(account, passwd)
        if re == "LOGIN_OK":
            # 初始化登录后的主界面
            self.mainwindow = Ui_ViewMain(account,self.sockfd)
            self.mainwindow.open_self()
            self.close()
        elif re == "CONNECT_FAILED":
            # 登录失败显示
            self.login_failed.setText("网络链接失败")
            self.login_failed.setHidden(False)
        else:
            self.login_failed.setText("登录失败...")
            self.login_failed.setHidden(False)

    def register(self):
        webbrowser.open("html/register.html")

    def retrieve(self):
        webbrowser.open("http://www.fcww12.com")

    def eventFilter(self, object, event):
        if object == self.close_button:
            if event.type() == QEvent.Enter:
                self.close_button.setStyleSheet(
                    "QPushButton{background-image: url(res/login/关闭点击.png)} QPushButton{border:none;}")
            if event.type() == QEvent.Leave:
                self.close_button.setStyleSheet(
                    "QPushButton{background-image: url(res/login/关闭悬浮.png)} QPushButton{border:none;}")
        if object == self.min_button:
            if event.type() == QEvent.Enter:
                self.min_button.setStyleSheet(
                    "QPushButton{background-image: url(res/login/最小化点击.png)} QPushButton{border:none;}")
            if event.type() == QEvent.Leave:
                self.min_button.setStyleSheet(
                    "QPushButton{background-image: url(res/login/最小化悬浮.png)} QPushButton{border:none;}")
        if object == self.login_button:
            if event.type() == QEvent.Enter:
                self.login_button.setStyleSheet(
                    "QPushButton{background-image: url(res/login/登陆点击.png)} QPushButton{border:none;}")
            if event.type() == QEvent.Leave:
                self.login_button.setStyleSheet(
                    "QPushButton{background-image: url(res/login/登陆悬浮.png)} QPushButton{border:none;}")
        return QWidget.eventFilter(self, object, event)

    def keyPressEvent(self, event):
        if event.key() == 16777220 or event.key() == 16777221:
            self.login()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sockfd = connect_server()
    login = ViewLogin(sockfd)
    login.show()
    sys.exit(app.exec_())

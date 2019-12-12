import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication

from TCP_client import search_user, add_friend, agree_add_friend
from view.view_widget import Widget


class Ui_SearchView(Widget):
    def __init__(self,account):
        super().__init__()
        self.account = account
        self.search_account=""
        self.setupUi()
    def setupUi(self):
        self.setObjectName("SearchView")
        self.resize(291, 514)
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(10, 80, 200, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(240, 80, 41, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.search)
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(0, 140, 288, 71))
        self.frame.setStyleSheet("border:none;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 25, 100, 17))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 20, 41, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.hide()
        self.pushButton_2.clicked.connect(self.do_add)

        self.pushButton_agree = QtWidgets.QPushButton(self.frame)
        self.pushButton_agree.setGeometry(QtCore.QRect(230, 20, 41, 25))
        self.pushButton_agree.setObjectName("pushButton_2")
        self.pushButton_agree.setText("同意")
        self.pushButton_agree.hide()
        self.pushButton_agree.clicked.connect(self.agree_add)

        self.pushButton_ignore = QtWidgets.QPushButton(self.frame)
        self.pushButton_ignore.setGeometry(QtCore.QRect(166, 20, 51, 25))
        self.pushButton_ignore.setObjectName("pushButton_2")
        self.pushButton_ignore.setText("忽略")
        self.pushButton_ignore.hide()

        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(260, 0, 34, 34))
        self.pushButton_3.setText("")
        self.pushButton_3.setStyleSheet(
            "QPushButton{border-image: url(res/login/guanbi.png)} QPushButton{border:none;}")
        self.pushButton_3.clicked.connect(self.close)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self)
        self.pushButton_4.setGeometry(QtCore.QRect(225, 0, 34, 34))
        self.pushButton_4.setText("")
        self.pushButton_4.setStyleSheet(
            "QPushButton{background-image: url(res/login/最小化.png)} QPushButton{border:none;}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.showMinimized)
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 67, 17))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def agree_add(self):
        agree_add_friend(self.account,self.search_account)
        self.label.setText("")
        self.pushButton_agree.hide()
        self.pushButton_ignore.hide()
        self.close()

    def show_result(self,msg):
        if msg == "NO":
            self.label.setText("没有查找到此用户")
        else:
            self.label.setText(msg)
            self.pushButton_2.show()

    def do_add(self):
        add_friend(self.account,self.search_account)
        self.label.setText("")
        self.pushButton_2.hide()
        self.close()

    def search(self):
        self.search_account = self.lineEdit.text()
        search_user(self.search_account)

    def retranslateUi(self, SearchView):
        _translate = QtCore.QCoreApplication.translate
        SearchView.setWindowTitle(_translate("SearchView", "Form"))
        self.pushButton.setText(_translate("SearchView", "搜索"))
        self.pushButton_2.setText(_translate("SearchView", "添加"))
        self.label_2.setText(_translate("SearchView", "搜索好友"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Ui_SearchView("admin")
    login.show()
    sys.exit(app.exec_())
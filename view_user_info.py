


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
import sys

from TCP_client import upload_head_img, connect_server
from model_user import User
from view_widget import Widget


class Ui_ViewUserInfo(Widget):
    def __init__(self,user):
        super().__init__()
        self.user = user
        self.filepath = ""
        self.setupUi()
    def setupUi(self):
        self.setObjectName("UserInfoView")
        self.resize(530, 354)
        self.setStyleSheet("background-color: white;")

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(180, 60, 41, 17))
        self.label.setObjectName("label")
        #头像按钮
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(250, 40, 61, 61))
        if self.user.img == "" or self.user.img is None:
            self.pushButton.setStyleSheet("border:none;border-image: url(res/main/椭圆 1.png);")
        else:
            self.pushButton.setStyleSheet("border:none;border-image: url(res/client_head_image/%s);"%self.user.img)
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.set_img)

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(180, 200, 67, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(180, 140, 67, 17))
        self.label_3.setObjectName("label_3")
        # 昵称
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(230, 140, 113, 25))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText(self.user.nickname)
        # 修改按钮
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 270, 89, 25))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.update_info)
        # 取消按钮
        self.pushButton_3 = QtWidgets.QPushButton(self)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 270, 89, 25))
        self.pushButton_3.setStyleSheet("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.close)
        # 性别
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(240, 200, 86, 25))
        self.comboBox.setStyleSheet("background-color: rgb(114, 159, 207);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def set_img(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,
                                                                "选取文件",
                                                                "/home/tarena/",  # 起始路径
                                                                "All Files(*.jpg)")  # 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            print("\n取消选择")
            return
        self.user.img = fileName_choose.split("/")[-1]
        self.filepath = fileName_choose
        print(self.user.img)
        print(self.filepath)

    def update_info(self):
        sex = self.comboBox.currentText()
        if sex == "男":
            self.user.sex = "m"
        else:
            self.user.sex = "w"
        upload_head_img(self.filepath,self.user.img)

    def retranslateUi(self, UserInfoView):
        _translate = QtCore.QCoreApplication.translate
        UserInfoView.setWindowTitle(_translate("UserInfoView", "Form"))
        self.label.setText(_translate("UserInfoView", "头像:"))
        self.label_2.setText(_translate("UserInfoView", "性别:"))
        self.label_3.setText(_translate("UserInfoView", "昵称:"))
        self.pushButton_2.setText(_translate("UserInfoView", "修改"))
        self.pushButton_3.setText(_translate("UserInfoView", "取消"))
        self.comboBox.setItemText(0, _translate("UserInfoView", "男"))
        self.comboBox.setItemText(1, _translate("UserInfoView", "女"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    connect_server()
    user= User(aaccount_id="admin",nickname="彭琦",img="admin.jpg")
    login = Ui_ViewUserInfo(user)
    login.show()
    sys.exit(app.exec_())

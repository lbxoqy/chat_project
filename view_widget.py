"""
所有界面的父类,可以隐藏窗口栏,还可以鼠标拖动
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.moveflag = False

    # 用于窗口移动
    def mousePressEvent(self, QMouseEvent):
        self.moveflag = True
        self.mouseX = QMouseEvent.globalX()
        self.mouseY = QMouseEvent.globalY()
        self.windowX = self.x()
        self.windowY = self.y()

    # 用于窗口移动
    def mouseMoveEvent(self, QMouseEvent):
        if self.moveflag == True:
            distX = QMouseEvent.globalX() - self.mouseX
            distY = QMouseEvent.globalY() - self.mouseY
            self.move(self.windowX + distX, self.windowY + distY)

    # 用于窗口移动
    def mouseReleaseEvent(self, QMouseEvent):
        self.moveflag = False

"""
Pyqt5界面的工具
"""
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QPushButton, QLineEdit


class PyqtTools:

    @staticmethod
    def set_button(QWidget, url, size1, size2, move1, move2):
        """
        设置按钮
        :param url: 按钮图标地址
        :param size1: 按钮尺寸长
        :param size2: 按钮尺寸宽
        :param move1: 按钮移动横坐标
        :param move2: 按钮移动纵坐标
        :return:
        """
        button = QPushButton(QWidget)
        button.setIcon(QIcon(url))
        button.resize(size1, size2)
        button.move(move1, move2)
        button.setStyleSheet("border:none;")
        return button

    @staticmethod
    def set_LineEdit(QWidget, chang, gao, x, y, style):
        """
        设置输入框
        :param chang: 长
        :param gao: 宽
        :param x: 偏移x
        :param y: 偏移y
        :param style: style
        :return: line_edit
        """
        line_edit = QLineEdit(QWidget)
        line_edit.resize(chang, gao)
        line_edit.move(x, y)
        line_edit.setStyleSheet(style)
        return line_edit

    @staticmethod
    def set_background(QWidget,url):
        """
        设置QWidget的背景
        :param QWidget:
        :param url:
        :return:
        """
        pale = QPalette()
        pale.setBrush(QPalette.Background, QBrush(QPixmap(url)))
        QWidget.setPalette(pale)


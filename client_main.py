import sys

from PyQt5.QtWidgets import QApplication

from TCP_client import connect_server
from view_login import ViewLogin

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # 连接服务器
        sockfd = connect_server()
        # 初始化登录界面
        login = ViewLogin(sockfd)
        if sockfd == "LINK_FAILED":
            login.login_failed.setText("网络链接失败")
            login.login_failed.setHidden(False)
        # 显示登录界面
        login.show()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        sys.exit("客户端退出")
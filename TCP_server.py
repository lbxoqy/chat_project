"""
服务器端
"""
import json
import multiprocessing
import os
import signal
from socket import *
import sys
from multiprocessing import *
from time import sleep
from database_crud import DataBaseCRUD
from flask import *
import re

# 全局变量
from model_user import User

HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)
db = DataBaseCRUD()

# 上线后的用户和连接
online_user_connfd_dict = multiprocessing.Manager().dict()
online_user_list = multiprocessing.Manager().list()


def find_all_info_by_account(connfd, list_data):  # list_data = ["FIND_USER_INFO_BY_ACCOUNT","account"]
    account = list_data[1]
    user = db.find_all_info_by_account(account)
    if user == False:
        pass
    else:
        for acco in online_user_list:
            if acco == user.account_id:
                user.online_status = 1
        dict_user = user.__dict__
        json_user = json.dumps(dict_user)
        connfd.send(json_user.encode())


def do_login(connfd, list_data):  # list_data = ["LOGIN","account passwd"]
    account_passwd = list_data[1].split(" ")
    account = account_passwd[0]
    passwd = account_passwd[1]
    if account in online_user_list:
        msg = "LOGIN_FAILED"
        connfd.send(msg.encode())
    else:
        re = db.find_passwd_by_account(account)
        result = False
        if re == passwd:
            result = True
        if result == True:
            msg = "LOGIN_OK"
            connfd.send(msg.encode())
            online_user_list.append(account)
            for acco, connfd1 in online_user_connfd_dict.items():
                message = "FRIEND_ONLINE %s" % account
                connfd1.send(message.encode())
                sleep(0.2)
            online_user_connfd_dict[account] = connfd

        else:
            msg = "LOGIN_FAILED"
            connfd.send(msg.encode())


def download_img(connfd, list_data):
    file_path = "res/server_head_image/" + list_data[1]
    try:
        fr = open(file_path, "rb")
        filesize = str(os.path.getsize(file_path))
    except:
        fr = open("res/server_head_image/椭圆 1 拷贝.png", "rb")
        filesize = str(os.path.getsize("res/server_head_image/椭圆 1 拷贝.png"))
    msg = filesize
    connfd.send(msg.encode())
    data = connfd.recv(1024)
    for line in fr:
        connfd.send(line)
    fr.close()


def find_all_friend(connfd, list_data):
    list_friend_account = db.find_all_friends(list_data[1])
    json_list_friend_account = json.dumps(list_friend_account)
    connfd.send(json_list_friend_account.encode())


def do_exit(list_data):
    account = list_data[1]
    try:
        online_user_list.remove(account)
        del online_user_connfd_dict[account]
        for acco, connfd1 in online_user_connfd_dict.items():
            message = "FRIEND_ONLINE %s" % account
            connfd1.send(message.encode())
            sleep(0.2)
    except:
        print("删除online_user失败")


def send_chat(list_data):
    account_text = list_data[1].split(" ", 2)
    friend_account = account_text[1]
    message = "CHAT " + list_data[1]
    for acco, connfd1 in online_user_connfd_dict.items():
        if acco == friend_account:
            connfd1.send(message.encode())


def send_img(connfd, list_data):
    tmp = list_data[1].split(" ", 3)
    file_name = tmp[0]
    file_size = int(tmp[1])
    recv_account = tmp[2]
    send_account = tmp[3]
    filepath = "res/chat_img/%s" % file_name
    fw = open(filepath, "wb")
    file_total_size = file_size
    receive_size = 0
    while receive_size < file_total_size:
        data = connfd.recv(1024)
        receive_size += len(data)
        fw.write(data)
        fw.flush()
    fw.close()
    for acco, connfd1 in online_user_connfd_dict.items():
        if recv_account == acco:
            try:
                fr = open(filepath, "rb")
                filesize = str(os.path.getsize(filepath))
                msg = "SEND_CHAT_IMG %s %s %s %s" % (filesize, file_name, recv_account, send_account)
                connfd1.send(msg.encode())
                # data = connfd.recv(1024)
                for line in fr:
                    connfd1.send(line)
                fr.close()
            except:
                print("发送图片失败")
                continue


def handle(connfd):
    while True:
        try:
            data = connfd.recv(1024 * 1024)  # "关键字 后续内容"
            print(data.decode())

            if not data:
                break
            list_data = data.decode().split(" ", 1)  # ["关键字" "后续内容"]
            # 登录
            if list_data[0] == "LOGIN":  # list_data = ["LOGIN","account passwd"]
                do_login(connfd, list_data)
            elif list_data[0] == "FIND_USER_INFO_BY_ACCOUNT":  # list_data = ["FIND_USER_INFO_BY_ACCOUNT","account"]
                find_all_info_by_account(connfd, list_data)
            elif list_data[0] == "DOWNLOAD_IMG":  # list_data = ["DOWNLOAD_IMG","img"]
                download_img(connfd, list_data)
            elif list_data[0] == "FIND_ALL_FRIENDS":  # list_data = ["FIND_ALL_FRIENDS","account"]
                find_all_friend(connfd, list_data)
            elif list_data[0] == "EXIT":  # list_data = ["EXIT","account"]
                do_exit(list_data)
            elif list_data[
                0] == "SEND_CHAT":  # list_data = ['SEND_CHAT', 'admin admin1 李行 2019-12-02-13:09:28: 111111']
                send_chat(list_data)
            elif list_data[0] == "SEND_IMG":  # list_data = ['SEND_IMG', 'file_name size recv_account send_account']
                send_img(connfd, list_data)
            elif list_data[0] == "UPLOAD_HEAD_IMG":
                upload_head_img(connfd, list_data)
            elif list_data[0] == "UPDATE_USER_INFO":
                info_list = list_data[1].split(" ",3)
                account = info_list[0]
                img = info_list[1]
                nickname = info_list[2]
                sex = info_list[3]
                result = db.update_user_info(account,img,nickname,sex)
                for acco, connfd1 in online_user_connfd_dict.items():
                    message = "FLUSH_USER_INFO %s"
                    connfd1.send(message.encode())
                    sleep(0.2)


        except:
            print("接收消息出错")


def upload_head_img(connfd, list_data):
    img_name = list_data[1]
    filepath = "res/server_head_image/%s" % img_name
    fw = open(filepath, "wb")
    msg = connfd.recv(1024)
    file_total_size = int(msg.decode())
    receive_size = 0
    while receive_size < file_total_size:
        data = connfd.recv(1024)
        receive_size += len(data)
        fw.write(data)
        fw.flush()
    fw.close()


app = Flask(__name__)

@app.route("/")
def index_view():
    return render_template("index.html")

@app.route("/register")
def register_view():
    return render_template("register.html")

@app.route("/do_register",methods=["post", "get"])
def do_register():
    account = request.form.get("account")
    nickname = request.form.get("nickname")
    passwd = request.form.get("passwd")
    answer1 = request.form.get("answer1")
    answer2 = request.form.get("answer2")
    user = User(aaccount_id=account,password=passwd,nickname=nickname,answer1=answer1,answer2=answer2)
    result = db.insert_user_into_user_table(user)
    if result:
        return render_template("register_succed.html",nickname=nickname)
    else:
        return render_template("register_failed.html")

@app.route("/findpwd1")
def findpwd1():
    return render_template("refind_pwd_account.html")

@app.route("/do_find_pwd",methods=["post"])
def do_find_pwd():
    account = request.form.get("account")
    answer1 = request.form.get("answer1")
    answer2 = request.form.get("answer2")
    user_temp = db.find_all_info_by_account(account)
    if user_temp == False:
        return render_template("refind_pwd_failed.html")
    else:
        if answer1 == user_temp.answer1 and answer2 == user_temp.answer2:
            return render_template("refind_pwd_new_pwd.html",account=account)
        else:
            return render_template("refind_pwd_failed.html")

@app.route("/do_new_pwd",methods=["post"])
def do_new_pwd():
    account = request.form.get("account")
    passwd = request.form.get("pwd")
    result = db.update_user_passwd(account,passwd)
    if result:
        return render_template("refind_pwd_succed.html")
    else:
        return render_template("refind_pwd_failed.html")


def main():

    # 创建tcp套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端链接
    while True:
        try:
            c, addr = s.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue

        #  有客户链接
        p = Process(target=handle, args=(c,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid < 0:
            os._exit(0)
        elif pid == 0:
            app.run(host="176.215.133.105")
        else:
            main()
    except:
        print("退出")

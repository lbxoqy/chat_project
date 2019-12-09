"""
TCP连接的客户端
"""
import json
import os
from socket import *
from model_user import User
from time import sleep

sockfd = socket()  # 默认参数就是tcp
server_addr = ('127.0.0.1', 8888)


def connect_server():
    """
    连接服务器
    :return:
    """
    try:
        sockfd.connect(server_addr)
    except:
        print("服务器链接失败")
        return "LINK_FAILED"
    else:
        return sockfd


def do_login(account, passwd):
    """
    登录
    :param account:
    :param passwd:
    :return:
    """
    message = "LOGIN %s %s" % (account, passwd)
    try:
        sockfd.send(message.encode())  # 发送字节串
    except:
        return "CONNECT_FAILED"
    msg = sockfd.recv(1024)
    # 登录成功
    if msg.decode() == "LOGIN_OK":
        return "LOGIN_OK"
    # 登录失败
    else:
        return "LOGIN_FAILED"


def find_all_info_by_account(account):
    """
    通过账号发送给服务器返回user对象
    :param account:
    :return:
    """
    message = "FIND_USER_INFO_BY_ACCOUNT %s" % account
    try:
        sockfd.send(message.encode())  # 发送字节串
    except:
        return "CONNECT_FAILED"
    msg = sockfd.recv(1024)
    json_user = msg.decode()
    dict_user = json.loads(json_user)
    user = User()
    user.__dict__ = dict_user
    return user

def search_user(account):
    message = "SEARCH_USER %s" % account
    sockfd.send(message.encode())  # 发送字节串

def add_friend(self_account,friend_account):
    message = "ADD_FRIEND %s %s" % (self_account,friend_account)
    sockfd.send(message.encode())  # 发送字节串

def agree_add_friend(self_account,friend_account):
    message = "AGREE_ADD_FRIEND %s %s" % (self_account, friend_account)
    sockfd.send(message.encode())  # 发送字节串

def download_head_img_by_account(img):
    """
    从服务器下载头像图片
    :param img: 头像图片名称
    :return:
    """
    filepath = "res/client_head_image/%s" % img
    is_exist = os.path.exists(filepath)
    if is_exist == True:
        pass
    else:
        message = "DOWNLOAD_IMG %s" % img
        try:
            sockfd.send(message.encode())  # 发送字节串
        except:
            print("连接失败")
        fw = open(filepath, "wb")
        msg = sockfd.recv(1024)
        file_total_size = int(msg.decode())
        receive_size = 0
        sockfd.send(b"ok")
        while receive_size < file_total_size:
            data = sockfd.recv(1024)
            receive_size += len(data)
            fw.write(data)
            fw.flush()
        fw.close()


def upload_head_img(filepath, img_name):
    message = "UPLOAD_HEAD_IMG %s" % img_name
    sockfd.send(message.encode())
    try:
        fr = open(filepath, "rb")
    except:
        print("上传图片失败")
    filesize = str(os.path.getsize(filepath))
    msg = filesize
    sockfd.send(msg.encode())
    sleep(0.1)
    for line in fr:
        sockfd.send(line)
    fr.close()


def update_user_info(account_id, img, nickname, sex):
    print("TCP_client,sssssssssssssssss")
    message = "UPDATE_USER_INFO %s %s %s %s" %(account_id,img,nickname,sex)
    sockfd.send(message.encode())


def send_img(send_account, recv_account, filepath):
    file_name = filepath.split("/")[-1]
    try:
        fr = open(filepath, "rb")
        filesize = str(os.path.getsize(filepath))
        msg = "SEND_IMG %s %s %s %s" % (file_name, filesize, recv_account, send_account)
        sockfd.send(msg.encode())
        for line in fr:
            sockfd.send(line)
        fr.close()
    except:
        print("打开图片失败")


def find_all_friends(account):
    """
    通过账号查找所有好友
    :param account:
    :return:
    """
    message = "FIND_ALL_FRIENDS %s" % account
    try:
        sockfd.send(message.encode())  # 发送字节串
    except:
        return "CONNECT_FAILED"
    msg_json = sockfd.recv(1024 * 1204)
    list_friend_account = json.loads(msg_json.decode())
    list_friends = []
    if list_friend_account == False:
        return list_friends
    else:
        for account in list_friend_account:
            user = find_all_info_by_account(account)
            list_friends.append(user)
        return list_friends


def exit(account):
    """
    退出操作
    :param account:
    :return:
    """
    message = "EXIT %s" % account
    sockfd.send(message.encode())


def send_chat(account, friend_account, text):
    """
    发送聊天消息
    :param account:
    :param friend_account:
    :param text:
    :return:
    """
    message = "SEND_CHAT %s %s %s" % (account, friend_account, text)
    sockfd.send(message.encode())

# def recv_message(account):
#     message = "RECV_MESSAGE %s"%account
#     sockfd.send(message.encode())
#     json_list_message = sockfd.recv(1024)
#     list_message = json.loads(json_list_message) #list_message = ["text1","text2"...]
#     return list_message

# def recv_message_ok(account):
#     message = "RECV_MESSAGE_OK %s" % account
#     sockfd.send(message.encode())
#
# def is_flush_message(account):
#     message = "IS_FLUSH_MESSAGE %s" % account
#     sockfd.send(message.encode())
#     msg = sockfd.recv(1024)
#     if msg.decode()=="FLUSH_MESSAGE":
#         return True
#     else:
#         return False

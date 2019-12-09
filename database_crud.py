"""
所有对数据库的操作
"""
import hashlib
import pymysql
from model_user import User

class DataBaseCRUD:
    def __init__(self):
        self.db = pymysql.connect(host='localhost',
                                  port=3306,
                                  user='root',
                                  password='123456',
                                  database='chatproject',
                                  charset='utf8')
        self.cur = self.db.cursor()
        self.__salt = None
        self.__hash = None

    # def encrypt_password(self, password):
    #     """
    #     加密用户密码
    #     :param password: 用户密码明文
    #     :return: 密码密文
    #     """
    #     self.__salt = "8**$#@"
    #     self.__hash = hashlib.md5(self.__salt.encode())
    #     self.__hash.update(password.encode())
    #     password = self.__hash.hexdigest()
    #     return password

    def find_passwd_by_account(self, account):
        """
        通过账号查找用户密码
        :param account: 账号
        :return: 密码
        """
        sql = "select password from user_table where account_id=%s"
        if not self.cur.execute(sql, account):
            return False
        return self.cur.fetchone()[0]


    # 需要修改
    def find_all_info_by_account(self, account):
        """
        通过账号查找用户的所有个人信息(不返回密码)
        :param account: 账号
        :return: user类的实例化对象
        """
        sql = "select * from user_table where account_id=%s;"
        if not self.cur.execute(sql, account):
            return False
        tuple_result =self.cur.fetchone()
        user = User()
        user.pid = tuple_result[0]
        user.account_id = tuple_result[1]
        user.nickname = tuple_result[2]
        user.password = tuple_result[3]
        user.sex = tuple_result[4]
        user.img = tuple_result[5]
        user.offline_message = tuple_result[6]
        user.answer1 = tuple_result[7]
        user.answer2 = tuple_result[8]
        user.answer3 = tuple_result[9]
        user.online_status = tuple_result[10]
        return user

    # 需要修改
    def insert_user_into_user_table(self, user):
        """
        将用户插入数据库
        :param user:
        :return: True插入成功 False插入失败
        """

        sql = "insert into user_table(account_id,nickname,password,answer1,answer2) values(%s,%s,%s,%s,%s);"
        arg_list = [user.account_id,user.nickname,user.password,user.answer1,user.answer2]
        try:
            self.cur.execute(sql, arg_list)
            self.db.commit()
        except:
            self.db.rollback()
            return False
        else:
            return True

    def update_user_passwd(self,account,passwd):
        sql = "update user_table set password=%s where account_id=%s;"
        arg_list=[passwd,account]
        try:
            self.cur.execute(sql, arg_list)
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False
        else:
            return True

    # 需要修改
    def update_user_info(self,account_id, img, nickname, sex):
        """
        更新用户信息
        :param account: 用户账号
        :param user:
        :return: 成功/失败
        """
        sql = "update user_table set nickname=%s,sex=%s,img = %s where account_id=%s;"
        arg_list = [nickname,sex,img,account_id]
        try:
            self.cur.execute(sql, arg_list)
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False
        else:
            return True

    def find_pid_by_account(self, account):
        """
        根据用户account查找用户的pid
        :param account: 账号
        :return: pid
        """
        sql = "select pid from user_table where account_id=%s"
        if not self.cur.execute(sql, account):
            return False

        list_pid = list(self.cur.fetchone())
        list_pid = [str(x) for x in list_pid]
        return "".join(list_pid)

    def add_friend(self, account, friend_acc):
        """
        添加好友
        :param account: 自己的账号
        :param friend_acc: 好友的账号
        :return: True 添加成功False添加失败
        """
        u_id = self.find_pid_by_account(account)
        f_id = self.find_pid_by_account(friend_acc)

        sql = "insert into user_friend_table values(%s, %s);"
        sql2 = "insert into user_friend_table values(%s, %s);"
        try:
            self.cur.execute(sql, (u_id, f_id))
            self.cur.execute(sql, (f_id, u_id))
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False
        else:
            return True

    def delete_friend(self, account, friend_acc):
        """
        根据自己的账号删除好
        :param account:
        :param friend_acc:
        :return: True 删除成功False删除失败
        """
        u_id = self.find_pid_by_account(account)
        print(u_id)
        f_id = self.find_pid_by_account(friend_acc)
        print(f_id)
        sql = "delete from user_friend_table where u_id=%s and f_id=%s"
        try:
            self.cur.execute(sql, [u_id, f_id])
            self.db.commit()
            return False
        except:
            return True

    # 需要修改
    def find_all_friends(self, account):
        """
        通过用户名查找该用户的所有好友
        :param account:
        :return: list类型,[account1,account2....]
        """
        list_friend = []
        u_id = self.find_pid_by_account(account)

        sql = "select f_id from user_friend_table where u_id=%s"
        if not self.cur.execute(sql, u_id):
            return False

        sql = "select account_id from user_table where pid=%s"
        for f_id in list(self.cur.fetchall()):
            f_id = [str(x) for x in f_id]
            if not self.cur.execute(sql, "".join(f_id)):
                return False
            list_friend.append(self.cur.fetchone()[0])
        return list_friend


    def find_all_offline_message(self, account):
        """
        通过账号查找到该用户的所有离线消息
        :param account:
        :return: list类型 [(message1,img1),(message2,img2)...]
        """
        u_id = self.find_pid_by_account(account)
        sql = "select message,img from user_offline_message_table where u_id=%s"
        if not self.cur.execute(sql, u_id):
            return False
        return list(self.cur.fetchall())

    def clear_offline_message(self, account):
        """
        删除所有离线消息
        :param account:
        :return:
        """
        u_id = self.find_pid_by_account(account)

        sql = "delete from user_offline_message_table where u_id=%s"
        try:
            self.cur.execute(sql, u_id)
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False
        else:
            return True

    def set_online_status(self, account, status=False):
        """
        设置用户的在线状态
        :param account: 用户的account
        :param status: 要设置的状态
        :return: True设置成功 False设置失败
        """
        sql = "update user_table set online_status = %s where account_id = %s;"
        arg_list = [status,account]

        try:
            self.cur.execute(sql, arg_list)
            self.db.commit()
        except Exception:
            self.db.rollback()
            return False
        else:
            return True

    def search_online_status(self, account):
        """
        返回用户的在线状态
        :param account:
        :return: 在线状态
        """
        pass

    def add_group(self, group_name):
        """
        创建群组
        :param group_name: 群名字
        :return:
        """
        pass

    def find_all_group_online_user(self, group_id):
        """
        根据群号查询所有在线的成员
        :param group_id: 群号
        :return: list类型 [user1,user2..]
        """
        pass

    def find_all_group_offline_user(self, group_id):
        """
        根据群号查询所有在线的不在线的成员
        :param group_id: 群号
        :return: list类型 [user1,user2..]
        """
        pass


if __name__ == '__main__':
    crud = DataBaseCRUD()
    # re = crud.find_all_info_by_account("admin")
    # re = crud.insert_user_into_user_table("admin2","lixing1","admin")
    # re = crud.update_user_info("admin2","李行","lixing93")
    # re = crud.find_pid_by_account("admin5")
    # re = crud.add_friend("admin","admin2")
    # re = crud.delete_friend("admin","admin2")
    re = crud.find_all_friends("admin")
    # re = crud.find_all_offline_message("admin1")
    # re = crud.clear_offline_message("admin1")
    print(re)

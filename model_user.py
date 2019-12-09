"""
用户类
"""


class User:
    def __init__(self, pid=0, aaccount_id="", nickname="", password="", sex="m", img="", offline_message=False,
                 answer1="", answer2="", answer3="", online_status=False):
        self.pid = pid
        self.account_id = aaccount_id
        self.nickname = nickname
        self.password = password
        self.sex = sex
        self.img = img
        self.offline_message = offline_message
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.online_status = online_status


if __name__ == '__main__':
    u1 = User(pid=100008)
    print(u1.pid)

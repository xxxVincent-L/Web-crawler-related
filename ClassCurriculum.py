import requests
import getpass

login_page = "http://zhjw.scu.edu.cn/login"
login_interface = "http://zhjw.scu.edu.cn/j_spring_security_check"  # 登录接口
login_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;\
    q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'zhjw.scu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/86.0.4240.111 Safari/537.36',
    "Referer": "http://zhjw.scu.edu.cn/login"
}


def userInfo():
    userId = input("请输入你的学号:\n")
    password = input("请输入你的密码:\n")

    # password = getpass.getpass('请输入你的密码:\n')
    print(userId)
    print(password)
    return userId, password


def login():
    userId, password = userInfo()

    post_data = {"j_username": userId, "j_password": password}
    session = requests.session()
    s = session.post(login_page, headers=login_header, data=post_data)  # 登录

    print(s.text)  # 只能看到frame部分的代码


if __name__ == '__main__':
    login()

# branch test
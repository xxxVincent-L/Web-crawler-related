import hashlib
import muggle_ocr
import requests
import getpass

sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

captcha_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
# login_page = "http://zhjw.scu.edu.cn/login"
login_interface = "http://zhjw.scu.edu.cn/j_spring_security_check"  # 登录接口
login_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;\
    q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'zhjw.scu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    "Referer": "http://zhjw.scu.edu.cn/login"
}


def userInfo():
    userId = input("请输入你的学号:\n")
    password = input("请输入你的密码:\n")

    # For test quickly
    # userId = "2019141450020"
    # password = ""

    # Hide what you input in the terminal
    # password = getpass.getpass('请输入你的密码:\n')

    print(userId)
    print(password)
    return userId, password


def login(session):
    userId, password = userInfo()

    original_captcha = session.get(url=captcha_url, headers=login_header).content

    processed_captcha_content = sdk.predict(image_bytes=original_captcha)
    print(processed_captcha_content)
    if len(processed_captcha_content) != 4:
        return None

    post_data = {"j_username": userId,
                 "j_password": hashlib.md5(password.strip('\n').encode()).hexdigest(),
                 "j_captcha": processed_captcha_content}

    # 搞错了post的第一个参数 -> 应该是那个需要进行安全判断的地方 而不是登录界面!!!
    s = session.post(login_interface, headers=login_header, data=post_data)  # Login

    print(s.text)

    if "欢迎" in s.text:
        return "success"
    else:
        return "failed"


if __name__ == '__main__':
    session = requests.session()
    while True:
        if login(session) == "success":
            print("成功了！")
            break
        else:
            print("失败了！")

# branch test

# how about more?

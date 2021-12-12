import hashlib
import json

import muggle_ocr
import requests
import getpass

sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

captcha_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
# login_page = "http://zhjw.scu.edu.cn/login"
login_interface = "http://zhjw.scu.edu.cn/j_spring_security_check"  # 登录接口
class_curriculum_url = "http://zhjw.scu.edu.cn/student/teachingResources/classCurriculum/searchCurriculumInfo/callback?planCode=2021-2022-2-1&classCode=193040301"

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


# get user's information
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


# user login
def userLogin(session):
    userId, password = userInfo()

    original_captcha = session.get(url=captcha_url, headers=login_header).content

    processed_captcha_content = sdk.predict(image_bytes=original_captcha)

    # print(processed_captcha_content)

    if len(processed_captcha_content) != 4:
        return None

    post_data = {"j_username": userId,
                 "j_password": hashlib.md5(password.strip('\n').encode()).hexdigest(),
                 "j_captcha": processed_captcha_content}

    # 搞错了post的第一个参数 -> 应该是那个需要进行安全判断的地方 而不是登录界面!!!
    response = session.post(login_interface, headers=login_header, data=post_data)  # Login

    print(response.text)

    if "欢迎" in response.text:
        return True
    else:
        return False


# data acquisition
def getUserClassCurriculum():
    response = session.get(class_curriculum_url, headers=login_header)
    class_curriculum_json = json.loads(response.text)
    # print(class_curriculum_json, type(class_curriculum_json))

    with open("ClassCurriculum.json", "w", encoding='utf-8') as f:
        json.dump(class_curriculum_json, f, indent=4, ensure_ascii=False)


# data process
def processData():
    curriculumList = []
    with open("ClassCurriculum.json", "r", encoding='utf-8') as f:
        rawData = json.load(f)

    rawDataList = rawData[0]
    lenOfCurriculum = len(rawDataList)

    for index in range(lenOfCurriculum):
        tempCourseList = rawDataList[index]

        tempCourseInfo = []

        courseName = tempCourseList["kcm"]
        tempCourseInfo.append(courseName)

        courseTeacher = tempCourseList["jsm"]
        tempCourseInfo.append(courseTeacher)

        coursePlace = tempCourseList["xqm"] + tempCourseList["jxlm"] + tempCourseList["jash"]
        tempCourseInfo.append(coursePlace)

        courseId = tempCourseList["id"]["kch"]
        tempCourseInfo.append(courseId)

        courseSequenceId = tempCourseList["id"]["kxh"]
        tempCourseInfo.append(courseSequenceId)

        courseWeek = tempCourseList["zcsm"]
        tempCourseInfo.append(courseWeek)

        courseDay = tempCourseList["id"]["skxq"]
        tempCourseInfo.append(courseDay)

        courseCredit = tempCourseList["xf"]
        tempCourseInfo.append(courseCredit)

        curriculumList.append(tempCourseInfo)

    return curriculumList



if __name__ == '__main__':
    session = requests.session()
    # while True:
    #     if userLogin(session):
    #         print("成功了！")
    #         getUserClassCurriculum()
    #         break
    #     else:
    #         print("失败了！")
    processData()

# test
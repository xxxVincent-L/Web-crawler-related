import hashlib
import json
from pymysql import *
import muggle_ocr
import requests
import getpass
import re
from pandas.tests.io.excel.test_openpyxl import openpyxl

sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)

# url preparation
captcha_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
# login_page = "http://zhjw.scu.edu.cn/login"
login_interface = "http://zhjw.scu.edu.cn/j_spring_security_check"  # 登录接口
raw_class_curriculum_url = "http://zhjw.scu.edu.cn/student/teachingResources/classCurriculum/searchCurriculumInfo/callback?classCode=193040301"
class_curriculum_url = ""

# header
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

    # For testing quick
    # userId = "2019141450020"
    # password = ""

    # Hide what you input in the terminal
    # password = getpass.getpass('请输入你的密码:\n')

    # print(userId)
    # print(password)
    return userId, password


# user login
def userLogin(session):
    userId, password = userInfo()  # get the information of users

    userPwd = hashlib.md5(password.strip('\n').encode()).hexdigest()  # Encryption

    original_captcha = session.get(url=captcha_url, headers=login_header).content

    processed_captcha_content = sdk.predict(image_bytes=original_captcha)

    # print(processed_captcha_content)

    if len(processed_captcha_content) != 4:
        return None

    # post data preparation
    post_data = {"j_username": userId,
                 "j_password": userPwd,
                 "j_captcha": processed_captcha_content}

    # 搞错了post的第一个参数 -> 应该是那个需要进行安全判断的地方 而不是登录界面!!!
    response = session.post(login_interface, headers=login_header, data=post_data)  # Login

    # print(response.text)

    if "欢迎" in response.text:
        return True
    else:
        return False


# data acquisition
def getUserClassCurriculum(class_curriculum_url):
    response = session.get(class_curriculum_url, headers=login_header)

    class_curriculum_json = json.loads(response.content.decode("utf-8"))

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


# store data as a excel table
def storeDataAsExcel():
    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append(["课程名",
               "上课教师",
               "上课地点",
               "课程号",
               "课序号",
               "上课周次",
               "上课星期",
               "学分"])

    curriculumList = processData()

    for course in curriculumList:
        print(course)
        ws.append(course)
    print("课程已经成功添加至Curriculum.xlsx!")

    wb.save('Curriculum.xlsx')  # Save


# store data as a DB's table
def storeDataAsDB():
    # If u wanna use the code, this part is what you should change.
    db = connect(host='localhost', port=3306, db='mydb', user='vincent', passwd='123456')
    cursor = db.cursor()
    curriculumList = processData()
    sqlOfCreateTable = '''
    CREATE TABLE IF NOT EXISTS `Curriculum` (
                                                课程名 varchar(50),
                                                上课教师 varchar(50),
                                                上课地点 varchar(50),
                                                课程号 varchar(50),
                                                课序号 varchar(50),
                                                上课周次 varchar(50),
                                                上课星期 int,
                                                学分 varchar(50)
    ) '''
    # print(sqlOfCreateTable)
    sqlOfInsertTable = '''insert into curriculum(课程名,
                                                上课教师,
                                                上课地点,
                                                课程号,
                                                课序号,
                                                上课周次,
                                                上课星期,
                                                学分
                                                ) values'''
    # print(sqlOfInsertTable)

    try:

        cursor.execute(sqlOfCreateTable)
        for course in curriculumList:
            tempSql = sqlOfInsertTable + "('" + course[0] + "','" + course[1] + "','" + course[2] + "','" + \
                      course[3] + "','" + course[4] + "','" + course[5] + "'," + str(course[6]) + ",'" + course[
                          7] + "')"
            # print(tempSql)
            cursor.execute(tempSql)

        db.commit()
        print("课程已经成功添加至数据库的Curriculum表中!")
        return True
    except Exception as e:
        print(e)
        db.rollback()
    return False


# choose the semester your wanna query
def chooseSemester():
    global plancode
    semester = input("你想查看哪个学期的课表？（标准输入为年份-季节：2021-秋）")

    infoOfSemester = re.split(r'\-', semester)
    year = infoOfSemester[0]
    season = infoOfSemester[1]

    seasonToInt = {"秋": 1, "春": 2}
    tempYear = 0
    if '秋' in season:
        tempYear = int(year) + 1
        plancode = str(year) + "-" + str(tempYear) + "-" + str(seasonToInt[season]) + "-1"

    elif '春' in season:
        tempYear = int(year) - 1
        plancode = str(tempYear) + "-" + str(year) + "-" + str(seasonToInt[season]) + "-1"

    class_curriculum_url = raw_class_curriculum_url + "&planCode=" + plancode
    print(class_curriculum_url)

    return class_curriculum_url


# The main call function of user's login
def mainCallOfLogin():
    while True:
        if userLogin(session):
            print("成功了！")
            getUserClassCurriculum(chooseSemester())
            break
        else:
            print("失败了！")


if __name__ == '__main__':
    session = requests.session()

    mainCallOfLogin()

    # storage
    storeDataAsExcel()
    storeDataAsDB()

import re
import random
import requests
import pytesseract

from PIL import Image
from lxml import etree
from threading import Thread

from CONFIG import *

session = requests.session()

def request_login_html(url):
    """
    请求登陆界面，获取form表单数据
    """
    try: 
        response = session.get(url=url, headers=HEADERS)
    except Exception as e:
        print("【请求失败】 原因：{0}".format(e))
        return None
    else:
        __VIEWSTATE = re.findall(r'id="__VIEWSTATE" value="(.*?)" />', response.text)
        __EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION" value="(.*?)" />', response.text)
        if __VIEWSTATE and __EVENTVALIDATION:
            return (__VIEWSTATE[0], __EVENTVALIDATION[0])
        else:
            print("【未能拿到提交数据】")
            print("【__VIEWSTATE】:{0}".format(__VIEWSTATE))
            print("__EVENTVALIDATION:{0}".format(__EVENTVALIDATION))
            return None

def request_check_code(url):
    """
    请求验证码图片,保存本地
    """
    try:
        response = session.get(url=url, headers=HEADERS)
    except Exception as e:
        print("【请求二维码失败】 原因：{0}".format(e))
    else:
        with open("checkCode.jpg", "wb") as file:
            file.write(response.content)

def show_code_img():
    """
    自动显示图片
    """
    image = Image.open("checkCode.jpg").convert('1')
    image.save("checkCode.png")
    image.show()
    

def login(url, postData, checkCode):
    """
    实现登陆
    """
    x = random.randint(30, 40)
    y = random.randint(15, 25)
    POSTDATA["__VIEWSTATE"] = postData[0]
    POSTDATA["__EVENTVALIDATION"] = postData[1]
    POSTDATA["CheckCode"] = checkCode
    POSTDATA["Btn_OK.x"] = x
    POSTDATA["Btn_OK.y"] = y

    try:
        response = session.post(url=url, data=POSTDATA, headers=HEADERS)
    except Exception as e:
        print("【登陆失败】 原因：{0}".format(e))
        return None
    else:
        if response.status_code == 200:
            return True

def return_score(url):
    """
    返回成绩
    """
    try:
        response = session.get(url=url, headers=HEADERS)
    except Exception as e:
        print("【发生错误】 原因：{0}".format(e))
        return None
    else:
        if response.status_code != 200:
            print("【或许验证码，账户，密码错误】")
            return None


    selector = etree.HTML(response.text)
    content = selector.xpath("//div[@id='divContent']//td/text()")

    for item in content:
        print(item)
    return True


if __name__ == "__main__":
    while True:
        postData = request_login_html(LOGIN_URL)
        if postData:
            request_check_code(CHECK_CODE_URL)
            
            # 为不堵塞程序，利用线程显示图片
            threadShowCodeImg = Thread(target=show_code_img)
            threadShowCodeImg.start()
            checkCode = input("【请输入验证码】：")
            if login(LOGIN_ACTION_URL, postData, checkCode):
                if return_score(SCORE_URL):
                    break


    print("【关闭图片可结束程序】")
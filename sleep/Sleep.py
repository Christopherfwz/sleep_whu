# -*- coding:utf-8 -*-
from pytesseract import image_to_string
from PIL import Image
import requests
import StringIO
from lxml import etree
import time

verifycode_url = "http://user-serv.whu.edu.cn:8080/selfservice/common/web/verifycode.jsp"
login_url = "http://user-serv.whu.edu.cn:8080/selfservice/module/scgroup/web/login_judge.jsf"
stop_page_url = "http://user-serv.whu.edu.cn:8080/selfservice/module/userself/web/self_suspend.jsf"
stop_request_url = "http://user-serv.whu.edu.cn:8080/selfservice/module/userself/web/self_suspend.jsf"

resume_page_url = "http://user-serv.whu.edu.cn:8080/selfservice/module/userself/web/self_resume.jsf"
resume_request_url = "http://user-serv.whu.edu.cn:8080/selfservice/module/userself/web/self_resume.jsf"


class Sleep:
    def __init__(self, username, password):
        self._requests = requests.Session()
        self._login_postdata = {
            "act": "add",
            "name": username,
            "password": password
        }
        self._stop_postdata = {
            "act": "init",
            "op": "suspend",
            "UserOperationForm": "UserOperationForm",
        }

        self._resume_postdata = {
            "act": "init",
            "op": "resume",
            "UserOperationForm": "UserOperationForm",
        }

        self._headers = {
            "Host": "user-serv.whu.edu.cn:8080",
            "Origin": "http://user-serv.whu.edu.cn:8080",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        }

    def _verifycode_recognize(self):
        # Requesting Verify Code
        res = self._requests.get(verifycode_url)
        io = StringIO.StringIO(res.content)
        img = Image.open(io)
        # img.show()
        a = image_to_string(img)
        return a

    def _login(self):
        """
        登录
        :return:
        """
        self._login_postdata["verify"] = self._verifycode_recognize()
        self._requests.post(login_url, self._login_postdata, headers=self._headers)

    def _stop(self):
        stop_page = self._requests.get(stop_page_url).text

        if u"已经处于暂停状态,无需再进行暂停!" in stop_page:
            return True

        html = etree.HTML(stop_page)
        self._stop_postdata["UserOperationForm:targetUserId"] = \
            html.xpath('//*[@id="UserOperationForm:targetUserId"]/@value')[0]
        self._stop_postdata["UserOperationForm:operationVerifyCode"] = \
            html.xpath('//*[@id="UserOperationForm:operationVerifyCode"]/@value')[0]
        self._stop_postdata["submitCodeId"] = html.xpath('//*[@id="submitCodeId"]/@value')[0]
        self._stop_postdata["UserOperationForm:verify"] = self._verifycode_recognize()
        self._stop_postdata["UserOperationForm:queryPassword_old"] = ""
        self._stop_postdata["com.sun.faces.VIEW"] = html.xpath('//*[@id="com.sun.faces.VIEW"]/@value')[0]
        self._stop_postdata["UserOperationForm:sus"] = html.xpath('//*[@id="UserOperationForm:sus"]/@value')[0]

        res = self._requests.post(stop_request_url, self._stop_postdata).text

        if u"alert('暂停用户" in res:
            return True
        else:
            return False

    def _resume(self):
        resume_page = self._requests.get(resume_page_url).text
        if u"已经处于正常状态,无需再进行恢复!" in resume_page:
            return True

        html = etree.HTML(resume_page)
        self._resume_postdata["UserOperationForm:targetUserId"] = \
            html.xpath('//*[@id="UserOperationForm:targetUserId"]/@value')[0]
        self._resume_postdata["UserOperationForm:operationVerifyCode"] = \
            html.xpath('//*[@id="UserOperationForm:operationVerifyCode"]/@value')[0]
        self._resume_postdata["submitCodeId"] = html.xpath('//*[@id="submitCodeId"]/@value')[0]
        self._resume_postdata["UserOperationForm:verify"] = self._verifycode_recognize()
        self._resume_postdata["UserOperationForm:queryPassword_old"] = ""
        self._resume_postdata["com.sun.faces.VIEW"] = html.xpath('//*[@id="com.sun.faces.VIEW"]/@value')[0]
        self._resume_postdata["UserOperationForm:res"] = html.xpath('//*[@id="UserOperationForm:res"]/@value')[0]

        res = self._requests.post(resume_request_url, self._resume_postdata).text

        if u"alert('恢复用户" in res:
            return True
        else:
            return False

    def keep(self, op):
        for i in range(5):
            try:
                self._login()
                if getattr(self, "_" + op)():
                    return True
                else:
                    time.sleep(5)
            except Exception as e:
                print e
                time.sleep(5)
        return False


if __name__ == '__main__':
    sleep = Sleep("2015302580060", "120018")
    # choice between "resume" and "stop"
    print sleep.keep("stop")

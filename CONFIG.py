"""
配置信息
"""

LOGIN_URL = "http://dekt.swpu.edu.cn/UserLogin.html"

CHECK_CODE_URL = "http://dekt.swpu.edu.cn/default3.html"

LOGIN_ACTION_URL = "http://dekt.swpu.edu.cn/UserLogin.html"

SCORE_URL = "http://dekt.swpu.edu.cn/SystemForm/WorkInfo.aspx"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1;\
						 WOW64) AppleWebKit/537.36 (KHT\
						 ML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",}

POSTDATA = {
	"__VIEWSTATE": "",
	"__EVENTVALIDATION": "",
	"UserName": "xxxxx", # 账户
	"UserPass": "xxxxx", # 密码
	"CheckCode": "",
	"Btn_OK.x": "",
	"Btn_OK.y": "",
}

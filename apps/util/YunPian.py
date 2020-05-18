import requests
import json


# 发送单挑短信
def send_single_sms(apikey, code, mobile):
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = f"【】您的验证码是{code}, 如非本人操作，请忽略本短信"

    # res = requests.post(url, data={
    #     "apikey": apikey,
    #     "mobile": mobile,
    #     "text": text
    # })
    # re_json = json.loads(res.text)
    return {
        "code": 0
    }


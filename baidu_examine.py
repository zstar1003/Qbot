import sys
import json
import base64

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
import ast

# 防止https证书校验不正确
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# 载入数据
with open("config.json", "r", encoding='utf-8') as jsonfile:
    config_data = json.load(jsonfile)
    API_KEY = config_data['baidu']['API_KEY']
    SECRET_KEY = config_data['baidu']['SECRET_KEY']
    IMAGE_CENSOR = config_data['baidu']['IMAGE_CENSOR']
    TEXT_CENSOR = config_data['baidu']['TEXT_CENSOR']
    TOKEN_URL = config_data['baidu']['TOKEN_URL']


# 获取token
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)

    result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()


"""
    读取文件
"""


def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""


def request_baidu(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)


if __name__ == '__main__':
    # 获取access token
    token = fetch_token()

    # 拼接文本审核url
    text_url = TEXT_CENSOR + "?access_token=" + token

    text = "我们要热爱自己"
    result = request(text_url, urlencode({'text': text}))
    print("----- 正常文本调用结果 -----")
    # str->dict
    new_dic = json.loads(result)
    print(new_dic['conclusion'])

    text = "我要爆粗口啦：百度AI真他妈好用"
    result = request(text_url, urlencode({'text': text}))
    print("----- 粗俗文本调用结果 -----")
    print(result)

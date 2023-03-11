import json
from baidu_examine import fetch_token, TEXT_CENSOR, request_baidu
from urllib.parse import urlencode
import time
import openai

# 接入百度API进行内容审核
def detect_txt(msg):
    # 获取access token
    token = fetch_token()
    # 拼接文本审核url
    text_url = TEXT_CENSOR + "?access_token=" + token
    result = request_baidu(text_url, urlencode({'text': msg}))
    print("审核结果：")
    # str->dict
    new_dic = json.loads(result)
    print(new_dic['conclusion'])
    if new_dic['conclusion'] != '合规':
        return True
    else:
        return False


def ask_gpt(msg):
    # OpenAi API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": msg}
        ]
    )
    result = json.loads(str(completion.choices[0].message))
    return result['content']


# 与ChatGPT交互
def chat(msg):
    # ChatGPT成功交互
    try:
        start_time = time.time()
        message = ask_gpt(msg)
        print("返回内容: ")
        print(message)
        end_time = time.time()
        # retult_message = message + '\n' + '回答用时:' + str(end_time - start_time) + '秒'
        retult_message = message
        # 返回之前，对输出内容进行检测
        # include_mgc = detect_txt(message)
        # # include_mgc = False
        # if include_mgc:
        #     retult_message = '你的问题疑似诱导Ai返回敏感内容，请尊重他人，注意自身言论'
        return retult_message
    # ChatGPT交互失败，调用本地GPT
    except Exception as error:
        print(error)
        retult_message = '服务器未正常响应，原因：' + str(error)
        return retult_message


# openai生成图片
def get_openai_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']
    print('图像已生成')
    print(image_url)
    return image_url
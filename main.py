import json
import time
from urllib.parse import urlencode
from urllib.request import Request
import requests
from flask import request, Flask
from revChatGPT.revChatGPT import Chatbot
import re
from sqltool import *
from baidu_shenhe_txt import fetch_token, TEXT_CENSOR, request_baidu
import openai


# 加载数据
with open("config.json", "r", encoding='utf-8') as jsonfile:
    config_data = json.load(jsonfile)
    cqhttp_url = config_data['qbot']['cqhttp_url']
    qq_no = config_data['qbot']['qq_no']
    openai.api_key = config_data['openai']['api_key']

# 创建一个服务，把当前这个python文件当做一个服务
server = Flask(__name__)


# 接入百度API进行文字检测
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


# 与ChatGPT交互的方法
def chat(msg):
    # ChatGPT成功交互
    try:
        # message = chatbot.get_chat_response(msg)['message']
        # 下面这行代码是获取对话id，如果你需要的话，id就是这么获取的
        # chatbot.conversation_id
        start_time = time.time()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=msg,
            temperature=0,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        message = response['choices'][0]['text']
        # message = uni_to_cn(response)
        print("返回内容: ")
        print(message)
        end_time = time.time()
        retult_message = message + '\n' + '回答用时:' + str(end_time - start_time) + '秒'
        # 返回之前，对输出内容进行检测
        include_mgc = detect_txt(message)
        if include_mgc:
            retult_message = '你的问题疑似诱导Ai返回涉黄涉政广告内容，请尊重他人，注意自身言论'
        return retult_message
    # ChatGPT交互失败，调用本地GPT
    except Exception as error:
        print(error)
        retult_message = '内容过长，超过4000个Token的最大输入'
        return retult_message


# 测试接口，可以测试本代码是否正常启动
@server.route('/', methods=["GET"])
def index():
    return f"你好，QQ机器人逻辑处理端已启动<br/>"


# qq消息上报接口，qq机器人监听到的消息内容将被上报到这里
@server.route('/', methods=["POST"])
def get_message():
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        sender = request.get_json().get('sender')  # 消息发送者的资料
        print("收到私聊消息：")
        print(message)
        msg_text = chat(message)  # 将消息转发给ChatGPT处理
        send_private_message(uid, msg_text)  # 将消息返回的内容发送给用户
    if request.get_json().get('message_type') == 'group':  # 如果是群消息
        gid = request.get_json().get('group_id')  # 群号
        uid = request.get_json().get('sender').get('user_id')  # 发言者的qq号
        message = request.get_json().get('raw_message')  # 获取原始信息
        # 判断当被@时才回答
        if str("[CQ:at,qq=%s]" % qq_no) in message:
            sender = request.get_json().get('sender')
            print("收到群聊消息：")
            print(message)
            # 敏感内容检测
            include_mgc = detect_txt(message)
            # 检查用户是否在数据库中
            if user_isexist(uid):
                # 用户存在，查询其剩余次数
                num_TextChance = select_TextChance(uid)
                if int(num_TextChance) == 0:
                    msg_text = "你今日次数已耗尽，请明日再来\nTips：讨好群主可解锁更多次数"
                    msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                else:
                    # 更新用户信息
                    update_user(uid, message)
                    if include_mgc:
                        clear_user(uid)
                        msg_text = '你的问题疑似包含涉黄涉政广告内容，今日剩余次数已被清空，请尊重他人，注意自身言论'
                        msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                    else:
                        msg_text = chat(message)  # 将消息转发给ChatGPT处理
                        msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text) + "\n你今日还剩%d次使用次数，请珍惜次数，问我一些有价值有意义的问题" % (int(num_TextChance)-1)  # @发言人
            else:
                # 加入新用户
                insert_user(uid, message)
                # 更新用户信息
                update_user(uid, message)
                if include_mgc:
                    clear_user(uid)
                    msg_text = '你的问题疑似包含涉黄涉政广告内容，今日剩余次数已被清空，请尊重他人，注意自身言论'
                    msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                else:
                    msg_text = chat(message)  # 将消息转发给ChatGPT处理
                    msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text) + "\n你今日还剩2次使用次数，请珍惜次数，问我一些有价值有意义的问题"  # @发言人
            send_group_message(gid, msg_text)  # 将消息转发到群里
    if request.get_json().get('post_type') == 'request':  # 收到请求消息
        print("收到请求消息")
        request_type = request.get_json().get('request_type')  # group
        uid = request.get_json().get('user_id')
        flag = request.get_json().get('flag')
        comment = request.get_json().get('comment')
        if request_type == "friend":
            print("收到加好友申请")
            print("QQ：", uid)
            print("验证信息", comment)
            # 直接同意，你可以自己写逻辑判断是否通过
            set_friend_add_request(flag, "false")
        if request_type == "group":
            print("收到群请求")
            sub_type = request.get_json().get('sub_type')  # 两种，一种的加群(当机器人为管理员的情况下)，一种是邀请入群
            gid = request.get_json().get('group_id')
            if sub_type == "add":
                # 如果机器人是管理员，会收到这种请求，请自行处理
                print("收到加群申请，不进行处理")
            elif sub_type == "invite":
                print("收到邀请入群申请")
                print("群号：", gid)
                # 直接同意，你可以自己写逻辑判断是否通过
                set_group_invite_request(flag, "false")
    return "ok"


# 发送私聊消息方法 uid为qq号，message为消息内容
def send_private_message(uid, message):
    try:
        res = requests.post(url=cqhttp_url + "/send_private_msg",
                            params={'user_id': int(uid), 'message': message}).json()
        if res["status"] == "ok":
            print("私聊消息发送成功")
        else:
            print(res)
            print("私聊消息发送失败，错误信息：" + str(res['wording']))

    except:
        print("私聊消息发送失败")


# 发送群消息方法
def send_group_message(gid, message):
    try:
        res = requests.post(url=cqhttp_url + "/send_group_msg",
                            params={'group_id': int(gid), 'message': message}).json()
        if res["status"] == "ok":
            print("群消息发送成功")
        else:
            print("群消息发送失败，错误信息：" + str(res['wording']))
    except:
        print("群消息发送失败")


# 处理好友请求
def set_friend_add_request(flag, approve):
    try:
        requests.post(url=cqhttp_url + "/set_friend_add_request", params={'flag': flag, 'approve': approve})
        print("处理好友申请成功")
    except:
        print("处理好友申请失败")


# 处理邀请加群请求
def set_group_invite_request(flag, approve):
    try:
        requests.post(url=cqhttp_url + "/set_group_add_request",
                      params={'flag': flag, 'sub_type': 'invite', 'approve': approve})
        print("处理群申请成功")
    except:
        print("处理群申请失败")


if __name__ == '__main__':
    server.run(port=7777, host='0.0.0.0')

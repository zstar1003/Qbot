import requests
from flask import request, Flask
from sqltool import *
from utils import *
import openai
from VITS import vits_infer

# 创建服务
server = Flask(__name__)

# 加载数据
with open("config.json", "r", encoding='utf-8') as jsonfile:
    config_data = json.load(jsonfile)
    cqhttp_url = config_data['qbot']['cqhttp_url']
    qq_no = config_data['qbot']['qq_no']
    openai_email = config_data['openai']['opai_email']
    openai_password = config_data['openai']['openai_password']
    openai.api_key = config_data['openai']['api_key']
    is_verify = config_data['baidu']['OPEN']


# 测试接口，可以测试本代码是否正常启动
@server.route('/', methods=["GET"])
def index():
    return f"你好，QQ机器人逻辑处理端已启动<br/>"


# qq消息上报接口，qq机器人监听到的消息内容将被上报到这里
@server.route('/', methods=["POST"])
def get_message():
    # 收到私聊信息，不做处理
    if request.get_json().get('message_type') == 'private':  # 如果是私聊信息
        # uid = request.get_json().get('sender').get('user_id')  # 获取信息发送者的 QQ号码
        message = request.get_json().get('raw_message')  # 获取原始信息
        # sender = request.get_json().get('sender')  # 消息发送者的资料
        print("收到私聊消息：")
        print(message)
    # 收到群消息，进行处理
    if request.get_json().get('message_type') == 'group':  # 如果是群消息
        gid = request.get_json().get('group_id')  # 群号
        uid = request.get_json().get('sender').get('user_id')  # 发言者的qq号
        message = request.get_json().get('raw_message')  # 获取原始信息
        # 判断当被@时才回答
        if str("[CQ:at,qq=%s]" % qq_no) in message:
            print("收到群聊消息：")
            print(message)
            message = str(message).replace(str("[CQ:at,qq=%s]" % qq_no), '')
            message = message.replace('"', "'")  # 双引号替换成单引号(防sql报错)
            # 敏感内容检测
            if is_verify:
                include_mgc = detect_txt(message)
            else:
                include_mgc = False
            # 前缀判断(用来区分是正常会话还是Ai绘图)
            if message.strip().startswith('生成图像'):
                message = str(message).replace('生成图像', '')
                # 检查用户是否在数据库中
                if user_isexist(uid):
                    # 用户存在，查询其剩余次数
                    num_PicChance = select_PicChance(uid)
                    if int(num_PicChance) == 0:
                        msg_text = "你当前次数已耗尽，向我提供新注册的OpenAi账号可享无限使用权"
                        msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                        send_group_message(gid, msg_text)  # 将消息转发到群里
                    else:
                        # 更新用户信息
                        update_user_pic(uid)
                        if include_mgc:
                            clear_user(uid)
                            msg_text = '你的问题疑似包含敏感内容，当前剩余次数已被清空，请尊重他人，注意自身言论'
                            msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                            send_group_message(gid, msg_text)  # 将消息转发到群里
                        else:
                            pic_path = get_openai_image(message)
                            msg_text = "你还剩%d次图像生成使用次数，Ai绘图成本较高，请珍惜次数" % (int(num_PicChance) - 1)  # @发言人
                            send_group_message_image(gid, pic_path, uid, msg_text)
                else:
                    # 加入新用户
                    insert_user(uid, message)
                    # 更新用户信息
                    update_user_pic(uid)
                    if include_mgc:
                        clear_user(uid)
                        msg_text = '你的问题疑似包含敏感内容，剩余次数已被清空，请尊重他人，注意自身言论'
                        msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                        send_group_message(gid, msg_text)  # 将消息转发到群里
                    else:
                        pic_path = get_openai_image(message)
                        msg_text = "你还剩3次图像生成使用次数，Ai绘图成本较高，请珍惜次数"
                        send_group_message_image(gid, pic_path, uid, msg_text)
            else:
                # 检查用户是否在数据库中
                if user_isexist(uid):
                    # 用户存在，查询其剩余次数
                    num_TextChance = select_TextChance(uid)
                    if int(num_TextChance) == 0:
                        msg_text = "你当前次数已耗尽，向我提供新注册的OpenAi账号可享无限使用权"
                        msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                        send_group_message(gid, msg_text)  # 将消息转发到群里
                    else:
                        # 更新用户信息
                        update_user(uid, message)
                        if include_mgc:
                            clear_user(uid)
                            msg_text = '你的问题疑似包含敏感内容，剩余次数已被清空，请尊重他人，注意自身言论'
                            msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                            send_group_message(gid, msg_text)  # 将消息转发到群里
                        else:
                            msg_text = chat(message)  # 将消息转发给ChatGPT处理
                            vits_infer.infer(msg_text)
                            # msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(
                            # msg_text) + "\n你还剩%d次使用次数，请珍惜次数，问我一些有价值有意义的问题" % (int(num_TextChance) - 1)  # @发言人
                            send_group_record(gid)
                else:
                    # 加入新用户
                    insert_user(uid, message)
                    # 更新用户信息
                    update_user(uid, message)
                    if include_mgc:
                        clear_user(uid)
                        msg_text = '你的问题疑似包含敏感内容，剩余次数已被清空，请尊重他人，注意自身言论'
                        msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(msg_text)
                        send_group_message(gid, msg_text)  # 将消息转发到群里
                    else:
                        msg_text = chat(message)  # 将消息转发给ChatGPT处理
                        vits_infer.infer(msg_text)
                        # msg_text = str('[CQ:at,qq=%s]\n' % uid) + str(
                        # msg_text) + "\n你还剩99次使用次数，请珍惜次数，问我一些有价值有意义的问题"  # @发言人
                        send_group_record(gid)

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
            # 直接拒接
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
                # 直接拒绝
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


# 发送文字信息
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


# 发送语音信息
def send_group_record(gid):
    try:
        v_path = r'file:///C:\Users\zxy\Desktop\QQ机器人\data\newtest.wav'
        message = "[CQ:record,file=" + v_path + "]"
        res = requests.post(url=cqhttp_url + "/send_group_msg",
                            params={'group_id': int(gid), 'message': message}).json()
        if res["status"] == "ok":
            print("群语音消息发送成功")
        else:
            print("群语音消息发送失败，错误信息：" + str(res['wording']))
    except:
        print("群语音消息发送失败")


# 发送图片信息
def send_group_message_image(gid, pic_path, uid, msg):
    try:
        message = "[CQ:image,file=" + pic_path + "]"
        if msg != "":
            message = msg + '\n' + message
        message = str('[CQ:at,qq=%s]\n' % uid) + message  # @发言人
        res = requests.post(url=cqhttp_url + "/send_group_msg",
                            params={'group_id': int(gid), 'message': message}).json()
        if res["status"] == "ok":
            print("群消息发送成功")
        else:
            print("群消息发送失败，错误信息：" + str(res['wording']))
    except Exception as error:
        print("群消息发送失败")
        print(error)


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

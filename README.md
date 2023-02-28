# Qbot
一个正在使用的Q群机器人项目

# 更新日志
2023-02-28
ChatGPT接口不稳定，换用Chatsonic聊天机器人，该产品单用户有最多25,000words的免费额度，将自己账户的key填充到后面的配置文件中即可使用。

官方文档：[https://docs.writesonic.com/reference/ans-my-ques_v2businesscontentans-my-ques_post](https://docs.writesonic.com/reference/ans-my-ques_v2businesscontentans-my-ques_post)

2023-02-11
上游重新支持ChatGPT逆向接口，ChatGPT机器人回归！

2022-12-25
加入DALL·E图像生成Api，并纳入数据库进行次数管理

2022-12-21
引入mysql数据库进行管理

2022-12-19 
首次提交代码，包含言论审核功能

更新进度后续将同步在我的CSDN博客：[https://blog.csdn.net/qq1198768105/category_12147929.html](https://blog.csdn.net/qq1198768105/category_12147929.html)

# 使用方式
1.安装配置mysql
在电脑上安装mysql，并参考 [博文](https://zstar.blog.csdn.net/article/details/128402216) 配置相关数据库和数据表

2.访问[百度Ai开放平台](https://ai.baidu.com/) ，创建内容审核应用，获取`API_KEY`和`SECRET_KEY`

3.修改`QBot/config.yml`中的QQ号

4.运行`QBot/go-cqhttp.bat`，弹出二维码扫码登陆

5.在根目录下新建`config.json`文件，该文件中各配置信息替换为自己的

```python
{
    "openai": {
        "api_key": "自己的",
        "opai_email": "自己的",
        "openai_password": "自己的"
    },
   "qbot": {
        "cqhttp_url": "http://localhost:8700",
        "qq_no": "自己机器人的"
    },
    "baidu": {
        "API_KEY": "自己的",
        "SECRET_KEY": "自己的",
        "IMAGE_CENSOR": "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined",
        "TEXT_CENSOR": "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined",
        "TOKEN_URL": "https://aip.baidubce.com/oauth/2.0/token"
    },
    "mysql": {
        "Root": "数据库用户名",
        "Password": "数据库密码"
    },
    "writesonic": {
        "Key": "自己的"
    }
}
```

6.先运行`QBot/go-cqhttp.bat`，在控制台扫码登录，再`main.py`，持续监听后台信息。


# To do
 - [x] 加入Ai绘图Api
 - [ ] 加入Ai图像超分
 - [ ] 加入Ai文字转语音

如果您有任何想法和建议，均可在此项目中提issue

# 用户使用方式
配置完成之后，将机器人拉到QQ群即可使用，目前支持两种方式：

- @机器人的方式来问问题，回复文本信息

- @机器人后，添加文字“生成图像”，后面加上描述语，回复Ai绘图图片信息。





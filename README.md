# Qbot
一个正在使用的Q群机器人项目

# 更新日志

2022-12-25
加入DALL·E图像生成Api，并纳入数据库进行次数管理

2022-12-21
引入mysql数据库进行管理

2022-12-19 
首次提交代码，包含言论审核功能

更新进度后续将同步在我的CSDN博客：[https://blog.csdn.net/qq1198768105/category_12147929.html](https://blog.csdn.net/qq1198768105/category_12147929.html)

# 使用方式
1.修改`QBot/config.yml`中的QQ号

2.运行`QBot/go-cqhttp.bat`，弹出二维码扫码登陆

3.在根目录下新建`config.json`文件，该文件中各配置信息替换为自己的

```python
{
    "openai": {
        "api_key": "openAi的api_key"
    },
   "qbot": {
        "cqhttp_url": "http://localhost:8700",
        "qq_no": "2986831742"
    },
    "baidu": {
        "API_KEY": "百度内容审核平台的API_KEY",
        "SECRET_KEY": "百度内容审核平台的SECRET_KEY",
        "IMAGE_CENSOR": "https://aip.baidubce.com/rest/2.0/solution/v1/img_censor/v2/user_defined",
        "TEXT_CENSOR": "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined",
        "TOKEN_URL": "https://aip.baidubce.com/oauth/2.0/token"
    }
}
```

4.运行`main.py`即可work


# To dox
 - [x] 加入Ai绘图Api
 - [ ] 加入Ai图像超分
 - [ ] 加入Ai文字转语音

如果您有任何想法和建议，均可在此项目中提issue

# 交流群
目前机器人部署在Q群：710413249，欢迎测试体验。





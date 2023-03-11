
# <div align="center">Qbot</div>

<div align="center">

一个正在使用的Q群机器人项目

![cover](assets/paimon.jpg)

致力于给电子宠物完整的一生

</div>


# 依赖环境
使用前需提前进行配置：

- chatgpt账号/apikey
  
- 数据库：Mysql

- 文字转语音：VITS

- (可选)文本内容审核：百度开放平台

# 使用方式
1.安装配置mysql
在电脑上安装mysql，并参考 [博文](https://zstar.blog.csdn.net/article/details/128402216) 配置相关数据库和数据表

2.访问[百度Ai开放平台](https://ai.baidu.com/) ，创建内容审核应用，获取`API_KEY`和`SECRET_KEY`

3.修改`QBot/config.yml`中的QQ号

4.运行`QBot/go-cqhttp.bat`，弹出二维码扫码登陆

5.在`config.json`文件中，将各配置信息替换为自己的

6.先运行`QBot/go-cqhttp.bat`，在控制台扫码登录，再`main.py`，持续监听后台信息。


# 用户使用方式
配置完成之后，将机器人拉到QQ群即可使用，目前支持两种方式：

- @机器人后，输入什么内容，它会将输入内容转换成语音输出。

- @机器人后，添加文字“生成图像”，后面加上描述语，回复Ai绘图图片信息。


# 更新日志
2023-03-11

将gpt3.5接口返回的信息和VITS结合，现在可以既发文字又发语音了，离完整的电子宠物又更近一步。

2023-03-10 

上线了VITS派蒙复读机，具体使用方式可参考我的另一仓库：[https://github.com/zstar1003/VITS](https://github.com/zstar1003/VITS)

2023-03-02

Chatsonic效果不好，弃用。

ChatGPT API发布，模型名为`gpt-3.5-turbo`，现已加入代码中

2023-02-28

ChatGPT接口不稳定，换用Chatsonic聊天机器人，该产品单用户有最多25,000words的免费额度。

2023-02-11

上游重新支持ChatGPT逆向接口，ChatGPT机器人回归！

2022-12-25

加入DALL·E图像生成Api，并纳入数据库进行次数管理

2022-12-21

引入mysql数据库进行管理

2022-12-19 

首次提交代码，包含言论审核功能

更新进度后续将同步在我的CSDN博客：[https://blog.csdn.net/qq1198768105/category_12147929.html](https://blog.csdn.net/qq1198768105/category_12147929.html)



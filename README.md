
# <div align="center">Qbot</div>

<div align="center">

一个曾经使用的Q群机器人项目

生卒年：2022-12-19 —— 2022-3-24

![cover](assets/paimon.jpg)

致力于给电子机器人完整的一生

<font size=3>注：只要不怕炸号，仍然可用 </font>

</div>

# 仓库状态
目前仓库已停止更新，因为我的QQ小号遭遇冻结，我无其它账号进行测试。

本仓库的初衷是利用Opai的技术来辅助群内答疑。因为交流群的目前的状态是提问的人多，回答的人少。此时，如果有一个机器人能够直接回答一些简单问题，这将极大解放答疑者时间以及减少提问者等待的时间。因此，**ChatGPT派蒙机器人**就这样上线了。

截至目前，机器人在上线期间，已服务上万人次，累计消耗Api费用17.88$。

因为种种原因，ChatGPT在国内无法直连使用，因此机器人也不断吸引各种人来“猎奇”，有些人会问所谓“敏感”问题。对此，对仓库进行了多轮迭代，引入百度平台的文本内容审核来规避风险。然而即便如此，仍然在今日下午被冻结。相关经验也供读者参考，请审慎使用本仓库的内容。

此次经历反映出，在这片“神奇”的土地上，想要免费地做一些公益是挺困难的。对我来说也是一种解放，每日维护Qbot状态的日子告一段落了。

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
2023-03-24

即使对内容进行了审核过滤，仍然于今日炸号(不排除被人恶意举报攻击的可能性)，因此，此项目将不再进行更新。

2023-03-11

将gpt3.5接口返回的信息和VITS结合，现在可以既发文字又发语音了。

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

![zhonghuaifang’s github stats](https://github-readme-stats.vercel.app/api?username=zhonghuaifang&show_icons=true&theme=merko)

<div align="center">
<h1 align="center">My-Actions</h1>
<img src="https://img.shields.io/github/issues/zhonghuaifang/My-Actions?color=8ab803">
<img src="https://img.shields.io/github/stars/zhonghuaifang/My-Actions?color=cda619">
<img src="https://img.shields.io/github/forks/zhonghuaifang/My-Actions?color=e97536">
<img src="https://img.shields.io/github/license/zhonghuaifang/My-Actions?color=ff69b4">
<img src="https://img.shields.io/github/languages/code-size/zhonghuaifang/My-Actions?color=7f2ace">
</div>

### 2022.11.15
修复任务判断语句导致自动执行时任务被跳过

### 2022.11.04
谢谢 @buiawpkgew1 提交的“删除旧的工作流运行”代码

### 2022.3.18

目前自用`贴吧签到`，`bilibil 签到`，`小米运动`，`电信签到`，其它自测

尝试修改代码中的时区，变量设置 `OS_TZ` 为时区数，例如中国设置 `8` 为 +8 区，默认 UTC +8（小米运动和哔哩哔哩签到可能需要，所以目前只在这两个脚本里添加了自定义时区）

### 2022.3.17

修复小米运动修改步数之后不同步到微信（github 的 actions 的执行时间为 UTC 0 时区，请参考下方[定时执行](#定时执行)自行更改）

个人收集并适配 Github Actions 的各类签到大杂烩

(签到项目备份，自用，加入了 cqhttp 通知，修复 b 站签到报错，原作者主页地址：https://github.com/BlueSkyClouds)

### 本项目已可以实现自动同步上游更改！[具体点击](#自动同步)

# 使用方式

1. 右上角 fork 本仓库
2. 点击 Settings -> Secrets -> 点击绿色按钮 (如无绿色按钮说明已激活。直接到第三步。)
3. 新增 new secret 并设置 Secrets:
4. 双击右上角自己仓库 Star 触发，如有不使用项目请[禁用部分项目](https://cdn.jsdelivr.net/gh/BlueskyClouds/BlueskyClouds.github.io/2020/10/19/img/2020-10-19.jpg)
5. **必须** - 请随便找个文件(例如`README.md`)，加个空格提交一下，否则可能会出现无法定时执行的问题
6. 由于规则更新,可能会 Fork 后会默认禁用,请手动点击 Actions 选择要签到的项目 `enable workflows`激活
7. [定时执行](#定时执行)

# 定时执行

1. 支持手动执行，具体在 Actions 中选中要执行的 Workflows 后再在右侧可以看到 Run workflow，点击即可运行此 workflow。

2. 如果嫌上一步麻烦的，也可以直接点击一下 star，你会发现所有的 workflow 都已执行。

3. 如需修改执行时间自行修改`.github\workflows\`下面的 yaml 内的`cron:` 执行时间为国际标准时间 [时间转换](http://www.timebie.com/cn/universalbeijing.php) 分钟在前 小时在后 尽量提前几分钟,因为下载安装部署环境需要一定时间

##### Cookie 变量设置 Secrets:\*\*

| 名称             | 内容                      | 说明                                                                                                                                                                            |
| ---------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PAT`            | 自动同步**必须设置**      | 利用 Github Actions 自动同步上游仓库或新建仓库[PAT 获取教程](RepoSync.md)                                                                                                       |
| `IQIYI_COOKIE`   | 爱奇艺 authcookie         | P00001 的值 详情[文字教程](https://www.bilibili.com/read/cv7437179) [视频教程](https://www.bilibili.com/video/BV1B541157DE) 电脑版有效期三个月                                  |
| `Xiaomi_User`    | 小米运动账号              | 小米运动账号,多账号请用#分割 例如：13800138000#13800138001                                                                                                                      |
| `Xiaomi_Pw`      | 小米运动密码              | 小米运动密码,多账号请用#分割 例如：abc123qwe#abcqwe2                                                                                                                            |
| `Xiaomi_Bs`      | 小米运动步数              | 默认为 1w-2w 之间随机 或自定义随机范围`[18000-25000]`                                                                                                                           |
| `BILI_USER`      | 哔哩哔哩账号              | B 站账号                                                                                                                                                                        |
| `BILI_PASS`      | 哔哩哔哩密码              | B 站密码                                                                                                                                                                        |
| `BILI_COOKIE`    | 哔哩哔哩 COOKIE`(非必填)` | 哔哩哔哩 COOKIE,如果账号密码无法登陆就用 COOKIE,等一段时间再用账号密码即可.                                                                                                     |
| `BILI_NUM`       | 哔哩哔哩每日投币数量      | 每日投币数量`可不填`默认 0 不投币                                                                                                                                               |
| `BILI_TYPE`      | 哔哩哔哩每日投币方式      | 投币方式`可不填`默认 1,只给关注的人投币 0 则随机投币                                                                                                                            |
| `BIKA_USER`      | 哔咔漫画用户名            | 哔咔漫画用户名                                                                                                                                                                  |
| `BIKA_PASS`      | 哔咔漫画密码              | 哔咔漫画密码                                                                                                                                                                    |
| `WPS_KEY`        | WPS_SID                   | WPS `COOKIE`中的 wps_sid,只要不注销,10 年过期                                                                                                                                   |
| `V_REF_URL`      | 腾讯视频 Request URL      | 电脑端搜索 auth_refresh 复制整段 Request url[图片教程](https://cdn.jsdelivr.net/gh/BlueskyClouds/BlueskyClouds.github.io/2020/11/1/img/v_1.jpg)                                 |
| `V_COOKIE`       | 腾讯视频 Cookie           | 电脑端搜索 auth_refresh 复制 Cookie[图片教程](https://cdn.jsdelivr.net/gh/BlueskyClouds/BlueskyClouds.github.io/2020/11/1/img/v_2.jpg)                                          |
| `TELECOM_MOBILE` | 中国电信手机号            | 只需要手机号 单账号 `多账号将会暴露手机号` 自行考虑,多账号使用`,`分割 部分地区或手机号暂无法签到，自行测试使用                                                                  |
| `V2EXCK`         | V2EX 的 Cookie            | V2EX 的 Cookie                                                                                                                                                                  |
| `BDUSS`          | 百度 BDUSS                | BDUSS 值切勿使用双击复制 (结尾有一个`符号`双击复制可能无法复制完整)                                                                                                             |
| `OS_TZ`          | 时区（自定义代码中时区）  | 默认`8`，小米运动和哔哩哔哩可能需要设置，不然上传可能不生效，国内设置`8`为 +8 时区（此处为代码中的时区设置，脚本运行请参考上方[定时执行](#定时执行)说明，定时执行时区不可能改） |

##### 推送通知环境变量(目前提供`微信server酱`、`pushplus(推送加)`、`iOS Bark APP`、`telegram机器人`、`钉钉机器人`、`企业微信机器人`、`iGot`等通知方式)

|       Name        |                                        归属                                         | 属性   | 说明                                                                                                                                                                                                                                                                           |
| :---------------: | :---------------------------------------------------------------------------------: | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|    `SEND_KEY`     |                                      推送开关                                       | 非必须 | 仅在 Cookie 失效时发送推送,值随意                                                                                                                                                                                                                                              |
|    `PUSH_KEY`     |                                 微信 server 酱推送                                  | 非必须 | server 酱的微信通知[更新公告](https://sc.ftqq.com/9.version)                                                                                                                                                                                                                   |
|    `BARK_PUSH`    | [BARK 推送](https://apps.apple.com/us/app/bark-customed-notifications/id1403753865) | 非必须 | IOS 用户下载 BARK 这个 APP,填写内容是 app 提供的`设备码`，例如：https://api.day.app/123 ，那么此处的设备码就是`123`，再不懂看 [这个图](https://github.com/BlueskyClouds/My-Actions/blob/master/icon/bark.jpg)（注：支持自建填完整链接即可）                                    |
|   `BARK_SOUND`    | [BARK 推送](https://apps.apple.com/us/app/bark-customed-notifications/id1403753865) | 非必须 | bark 推送声音设置，例如`choo`,具体值请在`bark`-`推送铃声`-`查看所有铃声`                                                                                                                                                                                                       |
|  `TG_BOT_TOKEN`   |                                    telegram 推送                                    | 非必须 | tg 推送(需设备可连接外网),`TG_BOT_TOKEN`和`TG_USER_ID`两者必需,填写自己申请[@BotFather](https://t.me/BotFather)的 Token,如`10xxx4:AAFcqxxxxgER5uw` , [具体教程](https://github.com/BlueskyClouds/My-Actions/blob/master/backUp/TG_PUSH.md)                                     |
|   `TG_USER_ID`    |                                    telegram 推送                                    | 非必须 | tg 推送(需设备可连接外网),`TG_BOT_TOKEN`和`TG_USER_ID`两者必需,填写[@getuseridbot](https://t.me/getuseridbot)中获取到的纯数字 ID, [具体教程](https://github.com/BlueskyClouds/My-Actions/blob/master/backUp/TG_PUSH.md)                                                        |
|  `DD_BOT_TOKEN`   |                                      钉钉推送                                       | 非必须 | 钉钉推送(`DD_BOT_TOKEN`和`DD_BOT_SECRET`两者必需)[官方文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq) ,只需`https://oapi.dingtalk.com/robot/send?access_token=XXX` 等于`=`符号后面的 XXX 即可                                                                      |
|  `DD_BOT_SECRET`  |                                      钉钉推送                                       | 非必须 | (`DD_BOT_TOKEN`和`DD_BOT_SECRET`两者必需) ,密钥，机器人安全设置页面，加签一栏下面显示的 SEC 开头的`SECXXXXXXXXXX`等字符 , 注:钉钉机器人安全设置只需勾选`加签`即可，其他选项不要勾选,再不懂看 [这个图](https://github.com/BlueskyClouds/My-Actions/blob/master/icon/DD_bot.png) |
|    `QYWX_KEY`     |                                 企业微信机器人推送                                  | 非必须 | 密钥，企业微信推送 webhook 后面的 key [详见官方说明文档](https://work.weixin.qq.com/api/doc/90000/90136/91770)                                                                                                                                                                 |
|     `QYWX_AM`     |                                  企业微信应用推送                                   | 非必须 | 依次填入 企业 id,secret,@all(或者成员 id),AgentID,图片 id [详见官方说明文档](https://work.weixin.qq.com/api/doc/90000/90135/90236) [详见获取教程文档](https://note.youdao.com/ynoteshare1/index.html?id=351e08a72378206f9dd64d2281e9b83b)                                      |
|  `IGOT_PUSH_KEY`  |                                      iGot 推送                                      | 非必须 | iGot 聚合推送，支持多方式推送，确保消息可达。 [参考文档](https://wahao.github.io/Bark-MP-helper)                                                                                                                                                                               |
| `PUSH_PLUS_TOKEN` |                                    pushplus 推送                                    | 非必须 | 微信扫码登录后一对一推送或一对多推送下面的 token(您的 Token) [官方网站](https://www.pushplus.plus/)                                                                                                                                                                            |
| `PUSH_PLUS_USER`  |                                    pushplus 推送                                    | 非必须 | 一对多推送的“群组编码”（一对多推送下面->您的群组(如无则新建)->群组编码）注:(1、需订阅者扫描二维码 2、如果您是创建群组所属人，也需点击“查看二维码”扫描绑定，否则不能接受群组消息推送)，只填`PUSH_PLUS_TOKEN`默认为一对一推送                                                    |
|  `TG_PROXY_HOST`  |                                 Telegram 代理的 IP                                  | 非必须 | 代理类型为 http。例子：http 代理 http://127.0.0.1:1080 则填写 127.0.0.1                                                                                                                                                                                                        |
|  `TG_PROXY_PORT`  |                                 Telegram 代理的端口                                 | 非必须 | 例子：http 代理 http://127.0.0.1:1080 则填写 1080                                                                                                                                                                                                                              |
|    `GOBOT_URL`    |                                    go-cqhttp URL                                    | 非必须 | 推送到个人 QQ: http://127.0.0.1/send_private_msg 群：http://127.0.0.1/send_group_msg                                                                                                                                                                                           |
|    `GOBOT_QQ`     |                                    go-cqhttp QQ                                     | 非必须 | 如果 GOBOT_URL 设置 /send_private_msg 则需要填入 user_id=个人 QQ 相反如果是 /send_group_msg 则需要填入 group_id=QQ 群                                                                                                                                                          |
|   `GOBOT_TOKEN`   |                                   go-cqhttp Token                                   | 非必须 | 填写在 go-cqhttp 文件设置的访问密钥                                                                                                                                                                                                                                            |

### 同步 Fork 后的代码

#### 手动同步

[手动同步 https://blog.blueskyclouds.com/jsfx/58.html](https://blog.blueskyclouds.com/jsfx/58.html)

#### 自动同步

##### 方案 A - 强制远程分支覆盖自己的分支

1. 参考[这里](https://github.com/zhonghuaifang/My-Actions/blob/master/backUp/gitSync.md)，安装[pull 插件](https://github.com/apps/pull)，并确认此项目已在 pull 插件的作用下（参考文中 1-d）。
2. 确保.github/pull.yml 文件正常存在，yml 内上游作者填写正确(此项目已填好，无需更改)。
3. 确保 pull.yml 里面是`mergeMethod: hardreset`(默认就是 hardreset)。
4. ENJOY!上游更改三小时左右就会自动发起同步。

##### 方案 B - 保留自己分支的修改

> 上游变动后 pull 插件会自动发起 pr，但如果有冲突需要自行**手动**确认。
> 如果上游更新涉及 workflow 里的文件内容改动，需要自行**手动**确认。

1. 参考[这里](https://github.com/zhonghuaifang/My-Actions/blob/master/backUp/gitSync.md)，安装[pull 插件](https://github.com/apps/pull)，并确认此项目已在 pull 插件的作用下（参考文中 1-d）。
2. 确保.github/pull.yml 文件正常存在，yml 内上游作者填写正确(此项目已填好，无需更改)。
3. 将 pull.yml 里面的`mergeMethod: hardreset`修改为`mergeMethod: merge`保存。
4. ENJOY!上游更改三小时左右就会自动发起同步。

### 鸣谢

特别感谢 [JetBrains](https://www.jetbrains.com/?from=My-Actions) 为开源项目提供免费的 [WebStrom](https://www.jetbrains.com/?from=My-Actions) 等 IDE 的授权  
[<img src="https://cdn.jsdelivr.net/gh/BlueskyClouds/BlueskyClouds.github.io/2020/12/1/img/idea/jetbrains.png" width="200"/>](https://www.jetbrains.com/?from=My-Actions)

## 历史 Star 数

[![Stargazers over time](https://starchart.cc/zhonghuaifang/My-Actions.svg)](https://starchart.cc/zhonghuaifang/My-Actions)


### 访问量

![](https://profile-counter.glitch.me/zhonghuaifang/count.svg)

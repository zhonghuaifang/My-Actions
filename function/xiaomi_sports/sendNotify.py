# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2

import sys
import os, re
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import base64
import hashlib
import hmac
import json
import threading
import time
import urllib.parse

import requests

# 通知服务
# fmt: off
push_config = {
    'BARK_PUSH': '',                    # bark IP 或设备码，例: https://api.day.app/DxHcxxxxxRxxxxxxcm/
    'BARK_ARCHIVE': '',                 # bark 推送是否存档
    'BARK_GROUP': '',                   # bark 推送分组
    'BARK_SOUND': '',                   # bark 推送声音

    'DD_BOT_SECRET': '',                # 钉钉机器人的 DD_BOT_SECRET
    'DD_BOT_TOKEN': '',                 # 钉钉机器人的 DD_BOT_TOKEN

    'FSKEY': '',                        # 飞书机器人的 FSKEY

    'GOBOT_URL': 'http://cqhttp.huaifang.top/send_private_msg',                    # go-cqhttp
                                        # 推送到个人QQ: http://127.0.0.1/send_private_msg
                                        # 群: http://127.0.0.1/send_group_msg
    'GOBOT_QQ': 'user_id=1459550455',                     # go-cqhttp 的推送群或用户
                                        # GOBOT_URL 设置 /send_private_msg 时填入 user_id=个人QQ
                                        #               /send_group_msg   时填入 group_id=QQ群
    'GOBOT_TOKEN': 'AwWCbD_1zZNZTlJ',                  # go-cqhttp 的 access_token

    'GOTIFY_URL': '',                   # gotify地址,如https://push.example.de:8080
    'GOTIFY_TOKEN': '',                 # gotify的消息应用token
    'GOTIFY_PRIORITY': 0,               # 推送消息优先级,默认为0

    'IGOT_PUSH_KEY': '',                # iGot 聚合推送的 IGOT_PUSH_KEY

    'PUSH_KEY': '',                     # server 酱的 PUSH_KEY，兼容旧版与 Turbo 版

    'PUSH_PLUS_TOKEN': '',              # push+ 微信推送的用户令牌
    'PUSH_PLUS_USER': '',               # push+ 微信推送的群组编码

    'QMSG_KEY': '',                     # qmsg 酱的 QMSG_KEY
    'QMSG_TYPE': '',                    # qmsg 酱的 QMSG_TYPE

    'QYWX_AM': '',                      # 企业微信应用

    'QYWX_KEY': '',                     # 企业微信机器人

    'TG_BOT_TOKEN': '',                 # tg 机器人的 TG_BOT_TOKEN，例: 1407203283:AAG9rt-6RDaaX0HBLZQq0laNOh898iFYaRQ
    'TG_USER_ID': '',                   # tg 机器人的 TG_USER_ID，例: 1434078534
    'TG_API_HOST': '',                  # tg 代理 api
    'TG_PROXY_AUTH': '',                # tg 代理认证参数
    'TG_PROXY_HOST': '',                # tg 机器人的 TG_PROXY_HOST
    'TG_PROXY_PORT': '',                # tg 机器人的 TG_PROXY_PORT
}


message_info = ''''''
push_config_s=dict()         # 整合通知服务本地和环境变量  


# 整合通知服务本地和环境变量
def initialize(d):
    global message_info,push_config_s
    message_info = ''''''
    for push_key in d.keys():   
        if push_key in os.environ and os.environ[push_key]:
            push_config_s[push_key]=os.environ[push_key]
        elif push_config[push_key]:
            push_config_s[push_key]=push_config[push_key]
        else:
            push_config_s[push_key]=d[push_key]
initialize(push_config)     # 初始化


def msg(*args):
    global message_info
    a=' '.join([str(arg) for arg in args])
    print(a)
    message_info = f"{message_info}\n{a}"
    sys.stdout.flush()


def bark(title: str, content: str) -> None:
    """
    使用 bark 推送消息。
    """
    if not push_config_s.get("BARK_PUSH"):
        print("bark 服务的 BARK_PUSH 未设置!!\n取消推送")
        return
    print("bark 服务启动")

    if push_config_s.get("BARK_PUSH").startswith("http"):
        url = f'{push_config_s.get("BARK_PUSH")}/{urllib.parse.quote_plus(title)}/{urllib.parse.quote_plus(content)}'
    else:
        url = f'https://api.day.app/{push_config_s.get("BARK_PUSH")}/{urllib.parse.quote_plus(title)}/{urllib.parse.quote_plus(content)}'

    bark_params = {
        "BARK_ARCHIVE": "isArchive",
        "BARK_GROUP": "group",
        "BARK_SOUND": "sound",
    }
    params = ""
    for pair in filter(
        lambda pairs: pairs[0].startswith("BARK_")
        and pairs[0] != "BARK_PUSH"
        and pairs[1]
        and bark_params.get(pairs[0]),
        push_config_s.items(),
    ):
        params += f"{bark_params.get(pair[0])}={pair[1]}&"
    if params:
        url = url + "?" + params.rstrip("&")
    response = requests.get(url).json()

    if response["code"] == 200:
        print("bark 推送成功!")
    else:
        print("bark 推送失败!")


# server酱
def serverJ(title: str, content: str) -> None:
    """
    通过 serverJ 推送消息。
    """
    if not push_config_s.get("PUSH_KEY"):
        print("serverJ 服务的 PUSH_KEY 未设置!!\n取消推送")
        return
    print("serverJ 服务启动")

    data = {"text": title, "desp": content.replace("\n", "\n\n")}
    if push_config_s.get("PUSH_KEY").index("SCT") != -1:
        url = f'https://sctapi.ftqq.com/{push_config_s.get("PUSH_KEY")}.send'
    else:
        url = f'https://sc.ftqq.com/${push_config_s.get("PUSH_KEY")}.send'
    response = requests.post(url, data=data).json()

    if response.get("errno") == 0 or response.get("code") == 0:
        print("serverJ 推送成功!")
    else:
        print(f'serverJ 推送失败!错误码: {response["message"]}')



# tg通知
def telegram_bot(title: str, content: str) -> None:
    """
    使用 telegram 机器人 推送消息。
    """
    if not push_config_s.get("TG_BOT_TOKEN") or not push_config_s.get("TG_USER_ID"):
        print("tg 服务的 bot_token 或者 user_id 未设置!!\n取消推送")
        return
    print("tg 服务启动")

    if push_config_s.get("TG_API_HOST"):
        url = f"https://{push_config_s.get('TG_API_HOST')}/bot{push_config_s.get('TG_BOT_TOKEN')}/sendMessage"
    else:
        url = (
            f"https://api.telegram.org/bot{push_config_s.get('TG_BOT_TOKEN')}/sendMessage"
        )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "chat_id": str(push_config_s.get("TG_USER_ID")),
        "text": f"{title}\n\n{content}",
        "disable_web_page_preview": "true",
    }
    proxies = None
    if push_config_s.get("TG_PROXY_HOST") and push_config_s.get("TG_PROXY_PORT"):
        if push_config_s.get("TG_PROXY_AUTH") is not None and "@" not in push_config_s.get(
            "TG_PROXY_HOST"
        ):
            push_config_s["TG_PROXY_HOST"] = (
                push_config_s.get("TG_PROXY_AUTH")
                + "@"
                + push_config_s.get("TG_PROXY_HOST")
            )
        proxyStr = "http://{}:{}".format(
            push_config_s.get("TG_PROXY_HOST"), push_config_s.get("TG_PROXY_PORT")
        )
        proxies = {"http": proxyStr, "https": proxyStr}
    response = requests.post(
        url=url, headers=headers, params=payload, proxies=proxies
    ).json()

    if response["ok"]:
        print("tg 推送成功!")
    else:
        print("tg 推送失败!")


def dingding_bot(title: str, content: str) -> None:
    """
    使用 钉钉机器人 推送消息。
    """
    if not push_config_s.get("DD_BOT_SECRET") or not push_config_s.get("DD_BOT_TOKEN"):
        print("钉钉机器人 服务的 DD_BOT_SECRET 或者 DD_BOT_TOKEN 未设置!!\n取消推送")
        return
    print("钉钉机器人 服务启动")

    timestamp = str(round(time.time() * 1000))
    secret_enc = push_config_s.get("DD_BOT_SECRET").encode("utf-8")
    string_to_sign = "{}\n{}".format(timestamp, push_config_s.get("DD_BOT_SECRET"))
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(
        secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
    ).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f'https://oapi.dingtalk.com/robot/send?access_token={push_config_s.get("DD_BOT_TOKEN")}&timestamp={timestamp}&sign={sign}'
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "text", "text": {"content": f"{title}\n\n{content}"}}
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=15
    ).json()

    if not response["errcode"]:
        print("钉钉机器人 推送成功!")
    else:
        print("钉钉机器人 推送失败!")


def qmsg_bot(title, content):
    """
    使用 qmsg 推送消息。
    """
    if not push_config_s.get("QMSG_KEY") or not push_config_s.get("QMSG_TYPE"):
        print("qmsg 的 QMSG_KEY 或者 QMSG_TYPE 未设置!!\n取消推送")
        return
    print("qmsg 服务启动")

    url = f'https://qmsg.zendee.cn/{push_config_s.get("QMSG_TYPE")}/{push_config_s.get("QMSG_KEY")}'
    payload = {"msg": f'{title}\n\n{content.replace("----", "-")}'.encode("utf-8")}

    try:
        response = requests.post(url=url, params=payload, timeout=15)
        try:
            datas = response.json()
            if response.get("code") == 0:
                print("qmsg 推送成功!")
            else:
                print(f'qmsg 推送失败!错误信息: {datas.get("reason")}')
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息: \n{traceback.format_exc()}")
    

# push+推送
def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 推送消息。
    """
    if not push_config_s.get("PUSH_PLUS_TOKEN"):
        print("PUSHPLUS 服务的 PUSH_PLUS_TOKEN 未设置!!\n取消推送")
        return
    print("PUSHPLUS 服务启动")

    url = "http://www.pushplus.plus/send"
    data = {
        "token": push_config_s.get("PUSH_PLUS_TOKEN"),
        "title": title,
        "content": content,
        "topic": push_config_s.get("PUSH_PLUS_USER"),
    }
    body = json.dumps(data).encode(encoding="utf-8")
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, data=body, headers=headers).json()

    if response["code"] == 200:
        print("PUSHPLUS 推送成功!")

    else:

        url_old = "http://pushplus.hxtrip.com/send"
        headers["Accept"] = "application/json"
        response = requests.post(url=url_old, data=body, headers=headers).json()

        if response["code"] == 200:
            print("PUSHPLUS(hxtrip) 推送成功!")

        else:
            print("PUSHPLUS 推送失败!")


# 企业微信 APP 推送
def wecom_app(title: str, content: str) -> None:
    """
    通过 企业微信 APP 推送消息。
    """
    if not push_config_s.get("QYWX_AM"):
        print("QYWX_AM 未设置!!\n取消推送")
        return
    QYWX_AM_AY = re.split(",", push_config_s.get("QYWX_AM"))
    if 4 < len(QYWX_AM_AY) > 5:
        print("QYWX_AM 设置错误!!\n取消推送")
        return
    print("企业微信 APP 服务启动")

    corpid = QYWX_AM_AY[0]
    corpsecret = QYWX_AM_AY[1]
    touser = QYWX_AM_AY[2]
    agentid = QYWX_AM_AY[3]
    try:
        media_id = QYWX_AM_AY[4]
    except IndexError:
        media_id = ""
    wx = WeCom(corpid, corpsecret, agentid)
    # 如果没有配置 media_id 默认就以 text 方式发送
    if not media_id:
        message = title + "\n\n" + content
        response = wx.send_text(message, touser)
    else:
        response = wx.send_mpnews(title, content, media_id, touser)

    if response == "ok":
        print("企业微信推送成功!")
    else:
        print("企业微信推送失败!错误信息如下: \n", response)

class WeCom:
    def __init__(self, corpid, corpsecret, agentid):
        self.CORPID = corpid
        self.CORPSECRET = corpsecret
        self.AGENTID = agentid

    def get_access_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        values = {
            "corpid": self.CORPID,
            "corpsecret": self.CORPSECRET,
        }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def send_text(self, message, touser="@all"):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": message},
            "safe": "0",
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]

    def send_mpnews(self, title, message, media_id, touser="@all"):
        send_url = (
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
            + self.get_access_token()
        )
        send_values = {
            "touser": touser,
            "msgtype": "mpnews",
            "agentid": self.AGENTID,
            "mpnews": {
                "articles": [
                    {
                        "title": title,
                        "thumb_media_id": media_id,
                        "author": "Author",
                        "content_source_url": "",
                        "content": message.replace("\n", "<br/>"),
                        "digest": message,
                    }
                ]
            },
        }
        send_msges = bytes(json.dumps(send_values), "utf-8")
        respone = requests.post(send_url, send_msges)
        respone = respone.json()
        return respone["errmsg"]


# 企业微信机器人
def wecom_bot(title: str, content: str) -> None:
    """
    通过 企业微信机器人 推送消息。
    """
    if not push_config_s.get("QYWX_KEY"):
        print("企业微信机器人 服务的 QYWX_KEY 未设置!!\n取消推送")
        return
    print("企业微信机器人服务启动")

    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={push_config_s.get('QYWX_KEY')}"
    headers = {"Content-Type": "application/json;charset=utf-8"}
    data = {"msgtype": "text", "text": {"content": f"{title}\n\n{content}"}}
    response = requests.post(
        url=url, data=json.dumps(data), headers=headers, timeout=15
    ).json()

    if response["errcode"] == 0:
        print("企业微信机器人推送成功!")
    else:
        print("企业微信机器人推送失败!")


# 飞书机器人
def feishu_bot(title, content):
    """
    使用 飞书机器人 推送消息。
    """
    if not push_config_s.get("FSKEY"):
        print("飞书 服务的 FSKEY 未设置!!\n取消推送")
        return
    print("飞书 服务启动")

    url = f'https://open.feishu.cn/open-apis/bot/v2/hook/{push_config_s.get("FSKEY")}'
    data = {"msg_type": "text", "content": {"text": f"{title}\n\n{content}"}}
    try:
        response = requests.post(url, data=json.dumps(data), timeout=15)
        try:
            datas = response.json()
            if datas.get("StatusCode") == 0:
                print("飞书 推送成功!")
            else:
                print(f"飞书 推送失败!响应数据: {datas}")
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息: \n{traceback.format_exc()}")

def go_cqhttp(title, content):
    """
    使用 go_cqhttp 推送消息。
    """
    if not push_config_s.get("GOBOT_URL") or not push_config_s.get("GOBOT_QQ") or not push_config_s.get("GOBOT_TOKEN"):
        print("go-cqhttp 服务的 GOBOT_URL 或 GOBOT_QQ 或 GOBOT_TOKEN 未设置!!\n取消推送")
        return
    print("go-cqhttp 服务启动")

    url = f'{push_config_s.get("GOBOT_URL")}?access_token={push_config_s.get("GOBOT_TOKEN")}&{push_config_s.get("GOBOT_QQ")}&message=标题:{title}\n内容:{content}'

    try:
        response = requests.get(url, timeout=15)
        try:
            datas = response.json()
            if datas.get("status") == "ok":
                print("go-cqhttp 推送成功!")
            else:
                print(f"go-cqhttp 推送失败!响应数据: {datas}")
        except json.JSONDecodeError:
            print(f"推送返回值非 json 格式，请检查网址和账号是否填写正确。\n{response.text}")
    except requests.exceptions.RequestException:
        print(f"网络异常，请检查你的网络连接、推送服务器和代理配置。\n{traceback.format_exc()}")
    except Exception:
        print(f"其他错误信息: \n{traceback.format_exc()}")


# gotify
def gotify(title:str,content:str)  -> None:
    """
    使用 gotify 推送消息。
    """
    if not push_config_s.get("GOTIFY_URL") or not push_config_s.get("GOTIFY_TOKEN"):
        print("gotify 服务的 GOTIFY_URL 或 GOTIFY_TOKEN 未设置!!\n取消推送")
        return
    print("gotify 服务启动")

    url = f'{push_config_s.get("GOTIFY_URL")}/message?token={push_config_s.get("GOTIFY_TOKEN")}'
    data = {"title": title,"message": content,"priority": push_config_s.get("GOTIFY_PRIORITY")}
    response = requests.post(url,data=data).json()

    if response.get("id"):
        print("gotify 推送成功!")
    else:
        print("gotify 推送失败!")


def iGot(title: str, content: str) -> None:
    """
    使用 iGot 推送消息。
    """
    if not push_config_s.get("IGOT_PUSH_KEY"):
        print("iGot 服务的 IGOT_PUSH_KEY 未设置!!\n取消推送")
        return
    print("iGot 服务启动")

    url = f'https://push.hellyw.com/{push_config_s.get("IGOT_PUSH_KEY")}'
    data = {"title": title, "content": content}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers).json()

    if response["ret"] == 0:
        print("iGot 推送成功!")
    else:
        print(f'iGot 推送失败!{response["errMsg"]}')


def send(title,text=''):
    """
    使用 bark, telegram bot, dingding bot, serverJ 发送手机推送
    :param title:
    :param content:
    :return:
    """
    if text:
        content=text+'\n'+message_info
    else:
        content=message_info
    content += '\nBy: https://github.com/wuye999/myScripts'

    if push_config_s['BARK_PUSH']:
        bark(title, content)

    if push_config_s['PUSH_KEY']:
        serverJ(title, content)

    if push_config_s['DD_BOT_TOKEN'] and push_config_s['DD_BOT_SECRET']:
        dingding_bot(title, content)

    if push_config_s['TG_BOT_TOKEN'] and push_config_s['TG_USER_ID']:
        telegram_bot(title, content)

    if push_config_s['QMSG_KEY'] and push_config_s['QMSG_TYPE']:
        qmsg_bot(title, content)

    if push_config_s['PUSH_PLUS_TOKEN']:
        pushplus_bot(title, content)

    if push_config_s['QYWX_AM']:
        wecom_app(title, content)

    if push_config_s.get("QYWX_KEY"):
        wecom_bot(title, content)

    if push_config_s['FSKEY']:
        feishu_bot(title, content)

    if push_config_s["GOBOT_URL"] and push_config_s["GOBOT_QQ"] and push_config_s['GOBOT_TOKEN']:
        go_cqhttp(title, content)

    if  push_config_s.get("GOTIFY_URL") and  push_config_s.get("GOTIFY_TOKEN"):
        gotify(title, content)

    if push_config_s.get("IGOT_PUSH_KEY"):
        iGot(title, content)


def main():
    send('title', 'content')


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-
import hashlib
import reply
import receive
import web
import urllib2
import re
from cityCode import CityCode
import json
import gzip
from StringIO import StringIO

class WeixinInterface:
    def GET(self):
        data = web.input()
        print(data)
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            print(data)
            token = "ding123thing" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                print(echostr)
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument


    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData   #后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    content = recMsg.Content
                    if content in CityCode:
                        str_wether = self.getWeather(content)
                        replyMsg = reply.TextMsg(toUser, fromUser, str_wether)
                        return replyMsg.send()
                    else:    
                        replyMsg = reply.TextMsg(toUser, fromUser, "我还在开发中。。嘤嘤嘤。。\n\n"+content)
                        return replyMsg.send()
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    # replyMsg = reply.TextMsg(toUser, fromUser, "我还在开发中。。嘤嘤嘤。。\n\n"+mediaId)
                    return replyMsg.send()
                elif recMsg.MsgType == 'event':
                    event = recMsg.Event
                    if event == 'subscribe':
                        replyMsg = reply.TextMsg(toUser, fromUser, "谢谢关注丁一二三事\n目前功能\n1.天气查询（eg.回复 松原天气）")
                        return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment

    def getWeather(self, cityName):
        cityCode = CityCode[cityName]
        url = "http://wthrcdn.etouch.cn/weather_mini?citykey=%s"%cityCode
        headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
           'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
        req = urllib2.Request(url, headers = headers)
        opener = urllib2.urlopen(req)
        html = opener.read()
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
        jStr = json.loads(data)
        detailWeather = ""
        pmAqi = jStr["data"].get("aqi", "")

        pmStr = ""
        if pmAqi != "":
            pmStr = "PM指数:"+pmAqi.encode("utf-8")
        for info in jStr["data"]["forecast"]:
            detailWeather = detailWeather + info["date"].encode("utf-8") + info["type"].encode("utf-8") + info["high"].encode("utf-8") + info["low"].encode("utf-8") + info["fengxiang"].encode("utf-8") + info["fengli"].encode("utf-8") + "\n"
        return jStr["data"]["city"].encode("utf-8")+" 当前温度: "+jStr["data"]["wendu"].encode("utf-8") + "℃," + pmStr + "\n" + jStr["data"]["ganmao"].encode("utf-8") + "\n未来几天:\n" + detailWeather

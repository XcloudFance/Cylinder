# -*- coding:utf-8 -*-
# encoding:utf-8
import os
import sys
import urllib
import urllib.parse
import urllib.request
import requests
import re
from bs4 import BeautifulSoup
from cut import *
import jsonpage
import pymysql
import socket, socketserver
import threading
import demjson
import json

hea = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "AspxAutoDetectCookieSupport=1",
    "Host": "jyj.quanzhou.gov.cn",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
}
mysqlconfig = {}
mysql = None
cursor = None


def togbk(string):
    return string.encode("gbk")


def delcssjs(code):
    while code.find("<style>") != -1:
        code = code[code.find("<style>") + len("<style>") : code.find("</style>")]
    while code.find("<script>") != -1:
        code = code[code.find("<script>") + len("<script>") : code.find("</script>")]
    while code.find('<script type="text/javascript">') != -1:
        code = code[
            code.find('<script type="text/javascript">')
            + len('<script type="text/javascript">') : code.find("</script>")
        ]
    return code


def gethtmurl(url):
    soup = BeautifulSoup(url, "html.parser")
    ret = []
    href_ = soup.find_all(name="a")
    for each in href_:
        if str(each.get("href"))[:4] == "http":
            ret.append(each.get("href"))
    return ret


def get_content(url):
    bs = BeautifulSoup(url, "html.parser")
    [s.extract() for s in bs(["script", "style"])]
    return bs.get_text().replace("\n", "").replace("\xa0", "")


dictlist = {}


def mainly(url):
    # print(delcssjs("<style>2333</style>123"))
    # url = "https://www.baidu.com/"#"http://jyj.quanzhou.gov.cn/2018hk/query_hk.aspx?hkksh=2879010326&hkxm=%E8%8B%8F%E7%82%9C%E5%AE%B8"
    #  req = urllib.request.Request(url=url, headers=headers)
    geturl = [url]
    # geturl = gethtmurl(url)
    # dictlist[url] = get_content(str(urllib.request.urlopen(req).read().decode('utf-8',"ignore")))
    length = 0
    while geturl != []:
        tmplist = geturl
        geturl = []
        # print(tmplist)
        # print(geturl)
        for i in tmplist:
            try:
                mysql.ping(reconnect=True)
                cursor.execute("select *")
                # req = urllib.request.Request(url=i, headers=headers)
                req = requests.get(i, hea)
                req.encoding = "utf-8"
                if i in dictlist:
                    continue
                if i.find(".png") != -1:
                    continue
                code = req.text  # urllib.request.urlopen(req).read()
                geturls = gethtmurl(code)
                tmpcode = code
                count = 0
                while 1 and count <= 100:
                    count += 1
                    tmpcode = get_content(
                        tmpcode
                    )  # .replace("\xa1","").replace('\u02d3',"").replace('\u0632',"")
                    if code != tmpcode:
                        code = tmpcode
                    else:
                        break
                dictlist[
                    i
                ] = (
                    code
                )  # get_content(str(code.decode('utf-8',"ignore"))).replace("\xa1","").replace('\u02d3',"").replace('\u0632',"")
                geturl += geturls
                wordlist = Cut(code)
                mysql.ping(reconnect=True)
                cursor.execute("select * from ")
            except:
                print(i + " :error")
            try:
                print(dictlist)
            except:
                print("编码错误")
                dictlist.pop(i)


def test():
    print(jsonpage.js001)


class server(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip().decode()
            print(self.data[:])
            jsonget = json.loads(self.data[:])
            print(jsonget)
            if jsonget["id"] == "001":
                global mysql, cursor
                mysqlconfig = jsonget["mysql"]
                mysql = pymysql.connect(
                    host=mysqlconfig["ip"],
                    password=mysqlconfig["password"],
                    user=mysqlconfig["username"],
                    port=int(mysqlconfig["port"]),
                )
                cursor = mysql.cursor()
            if jsonget["id"] == "002":
                threading.Thread(target=mainly, args=(jsonget["url"],)).start()
                self.request.send("null")  # 都是客户端返回结果
            print(mysqlconfig)
            self.request.send("None".encode("utf-8"))


if __name__ == "__main__":
    # test()

    HOST, PORT = "localhost", 1001
    server = socketserver.ThreadingTCPServer((HOST, PORT), server)
    server.serve_forever()

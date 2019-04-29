'''#-*- coding = utf-8 -*-
from bs4 import BeautifulSoup
testcode = "<html><p>正文内容</p><h1>标题</h1><script type='text/javascript'>alert('233')</script></html>"
bs = BeautifulSoup(testcode,'html.parser')
[s.extract() for s in bs(['script','style'])]#,'style')]
print(bs.get_text())'''
# coding=utf-8
import re
import urllib.request
import ssl
def getHtml(url):
       page = urllib.request.urlopen(url)
       html = page.read()
       html = html.decode('utf-8')
       return html
def getImg(html):
       reg = r'<p class="img_title">(.*)</p>'
       img_title = re.compile(reg)
       imglist = re.findall(img_title, html)
       return imglist
ssl._create_default_https_context = ssl._create_unverified_context
url = "https://tieba.baidu.com"
html = getHtml(url)
imglist = getImg(html)
print(imglist)

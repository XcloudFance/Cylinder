from bs4 import BeautifulSoup
def get_content(url):#注意此处的getcontent的url参数是url的htmlcode，不能直接填写url与gethtmurl函数不同
    bs = BeautifulSoup(url, "html.parser")
    return bs.get_text()
print(get_content("<title>233</title>\\n<h1>666</h1><h1>6626</h1><a href='233'>点击此处</a>"))
'''import pymysql
import sys
con = pymysql.connect(host = "localhost",user = 'root',passwd ='root',charset='utf-8')'''
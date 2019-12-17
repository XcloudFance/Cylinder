#-*- coding:gbk -*-
import socket
import json
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(("qpomelo.tw",4000))

while 1:
    msg = input('>>:').strip()
    if not msg:continue
    c.send(msg.encode('utf-8'))
    data = c.recv(1024)
    print(data.decode('utf-8'))
c.close()
'''json.loads() 字符串 to json
json.dumps() json to 字符串
当然json也可以用decode和encode来实现转码
json格式输出(方便调试):print(json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': ')))'''

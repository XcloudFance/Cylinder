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
'''json.loads() �ַ��� to json
json.dumps() json to �ַ���
��ȻjsonҲ������decode��encode��ʵ��ת��
json��ʽ���(�������):print(json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': ')))'''

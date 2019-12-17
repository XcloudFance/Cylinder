#encoding:utf-8
import json
import jsonpage
import time,datetime
import socket,socketserver
import threading
import demjson
log = {}
searchip = '127.0.0.1'
mysqljson={
	"ip":"cd-cdb-gf4to610.sql.tencentcdb.com",
	'port':'63791',
	'username' : 'root2',
	'password' : 'RGgPdrI4VhMc6Jhm9$@$'
}
redisip = '127.0.0.1'
status = {} #这里是对爬虫的status状态进行监控，例如正爬取什么网页的内容
class server(socketserver.BaseRequestHandler):
	def handle(self):
		while True:
			data = self.request.recv(1024).strip()
			self.request.send('null')#都是客户端返回结果
def t1():
	while True:
		cmd = input("CylinCommand-> ")
		cmd = cmd.split()
		if cmd[0] == 'log':
			if len(cmd) == 1:
				print(log)
				continue
			if cmd[1] == 'all':
				print(log)
			if cmd[1] == 'append':
				lctime = time.time()
				if lctime not in log:
					log[lctime] = cmd[2] + ","  # 用逗号分隔不同时间段log
				else:
					log[lctime] += cmd[2] + ","  # 用逗号分隔不同时间段log
			if cmd[1] == 'today':
				today = time.localtime(time.time()).tm_mday
				result=[]
				for i in log:
					if time.localtime(i).tm_mday == today:
						result.append(log[i])
				print(result)
		if cmd[0] == 'exit':
			exit(0)
		if cmd[0] == 'reset':
			if cmd[1] == 'search':#这里设置的是青荇搜索引擎的ip address
				searchip = cmd[2]
			if cmd[1] == 'redis':
				redisip = cmd[2]
			if cmd[1] == "mysql":
				mysqljson['ip'] = cmd[2]
				mysqljson['port'] = cmd[3]
		if cmd[0] == 'spider':
			if cmd[1] == 'reset':
				tuple = (cmd[2],cmd[3])
				status[tuple]='None'
				#此时是接入爬虫的时候，对爬虫发送一个client请求
				sock = socket.socket()
				sock.connect((cmd[2],int(cmd[3])))
				jsonsend = {'id':'001','mysql':mysqljson}
				#data = json.dumps(jsonsend)
				print(str(jsonsend))
				sock.send(json.dumps(jsonsend).encode('utf-8'))
				sock.recv(1024)
				sock.close()
			if cmd[1] == 'catch':
				url = cmd[2]
				#空闲状态的status会变成None
				for i in status:
					if status[i] == 'None':
						status[i] = url
						print(url)
						jsonsend={'id':'002','url':url}
						sock = socket.socket()
						sock.connect((i[0],int(i[1])))
						#data = json.dumps(jsonsend)
						sock.send(json.dumps(jsonsend).encode('utf-8'))


T1 = threading.Thread(target=t1).run()
HOST, PORT = "localhost", 2333
server = socketserver.ThreadingTCPServer((HOST, PORT), server)
server.serve_forever()
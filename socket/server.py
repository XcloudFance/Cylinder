import socketserver
import json
# 自定义类来实现通信循环
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            try:
                data = self.request.recv(1024)
                if not data: break
                print('->client:', data)
                print("{} wrote:".format(self.client_address))
                self.request.send(data)
            except ConnectionResetError:
                break
        self.request.close()
 
 
if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MyTCPHandler)
    server.serve_forever()


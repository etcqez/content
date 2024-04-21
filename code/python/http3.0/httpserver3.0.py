from socket import *
import sys
from threading import Thread
from config import *
import re,json

ADDR=(HOST,PORT)

# 和web frame通信的函数
def connect_frame(env):
    s=socket()
    try:
        s.connect((frame_ip,frame_port))
    except Exception as e:
        print(e)
        return
    data=json.dumps(env)
    s.send(data.encode())
    # 歉收来自webframe数据
    data=s.recv(4096*100).decode()
    return json.loads(data)

class HTTPServer:
    def __init__(self):
        self.address=ADDR
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd=socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)

    def bind(self):
        self.sockfd.bind(self.address)
        self.ip=self.address[0]
        self.port=self.address[1]

    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d'%self.port)
        while True:
            connfd,addr=self.sockfd.accept()
            print('Connect from',addr)
            client=Thread(target=self.handle,args=(connfd,))
            client.daemon
            client.start()

    def handle(self,connfd):
        request=connfd.recv(4096).decode()
        # 捕获组
        pattern=r'(?P<method>[A-Z]+)\s+(?P<info>/\S*)' 
        try:
            # 返回捕获组的组名和内容对应的字典
            env=re.match(pattern,request).groupdict() 
        except:
            connfd.close()
            return
        else:
            data=connect_frame(env)
            if data:
                self.response(connfd,data)

    # 给浏览器发送数据
    def response(self,connfd,data):
        # data => {'status':'200','data':'xxx'}
        if data['status']=='200':
            responseHeader='HTTP/1.1 200 OK\r\n'
            responseHeader+='Content-Type:text/html\r\n'
            responseHeader+='\r\n'
            responseBody=data['data']

        elif data['status']=='404':
            responseHeader='HTTP/1.1 404 Not Found\r\n'
            responseHeader+='Content-Type:text/html\r\n'
            responseHeader+='\r\n'
            responseBody=data['data']

        elif data['status']=='500':
            pass
        response_data=responseHeader+responseBody
        connfd.send(response_data.encode())

httpd=HTTPServer()
httpd.serve_forever()

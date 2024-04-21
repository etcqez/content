from socket import *
from threading import Thread
import sys,os
import time

HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)
FTP='/home/f/FTP/' # 文件库位置

# 创建类视而不见服务器文件处理功能
class FTPServer(Thread):
    '''
    查看列表,下载,上传,退出处理
    '''
    def __init__(self,connfd):
        self.connfd=connfd
        super().__init__()

    def do_list(self):
        files=os.listdir(FTP)
        if not files:
            self.connfd.send('文件库为空'.encode())
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
        # 拼接文件
        filelist=''
        for file in files:
            if file[0]!='.' and os.path.isfile(FTP+file):
                filelist += file+'\n'
        self.connfd.send(filelist.encode()) 

    def do_get(self,filename):
        try:
            f=open(FTP+filename,'rb')
        except Exception:
            self.connfd.send('文件不存在'.encode())
            return
        else:
            self.connfd.send(b'OK')
            time.sleep(0.1)
        while True:
            data=f.read(1024)
            if not data:
                time.sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)

    def do_put(self,filename):
        if os.path.exists(FTP+filename):
            self.connfd.send('文件存在'.encode())
            return
        else:
            self.connfd.send(b'OK')
        f=open(FTP+filename,'wb')
        while True:
            data=self.connfd.recv(1024)
            if data==b'##':
                break
            f.write(data)
        f.close()

    def run(self):
        while True:
            data=self.connfd.recv(1024).decode()
            if not data or data=='Q':
                return
            elif data=='L':
                self.do_list()
            elif data[0]=='G':
                filename=data.split(' ')[-1]
                self.do_get(filename)
            elif data[0]=='P':
                filename=data.split(' ')[-1]
                self.do_put(filename)

def main():
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    while True:
        try:
            c,addr=s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            break
            sys.exit('退出服务器')
    
        client=FTPServer(c)
        client.daemon
        client.start()

if __name__ == "__main__":
    main()

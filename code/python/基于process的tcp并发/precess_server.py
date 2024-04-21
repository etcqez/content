from socket import *
from multiprocessing import Process
import os
import signal

HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)

def handle(c):
    while True:
        data=c.recv(1024)
        if not data:
            break
        print(data.decode())
        c.send(b"OK")
    c.close()

s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

# 处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
print('Listen the port 8888...')

# 循环处理客户端请求
while True:
    try:
        c,addr=s.accept()
        print('Connect from',addr)
    except KeyboardInterrupt:
        os._exit(0)
    except Exception as e:
        print(e)
        continue
    # 创建子进程处理客户端事物
    p=Process(target=handle,args=(c,))
    p.daemon=True # 父进程结束则所有服务终止
    p.start()

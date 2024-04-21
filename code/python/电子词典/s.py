from socket import *
from multiprocessing import Process
import signal,sys
from mysql import Database
from time import sleep

HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)
db=Database(database='dict')

def do_query(c,data):
    tmp=data.split(' ')
    name=tmp[1]
    word=tmp[2]

    db.insert_hist(name,word)
    mean=db.query(word)
    if not mean:
        c.send('没有找到该单词'.encode())
    else:
        msg='%s : %s'%(word,mean)
        c.send(msg.encode())
def do_hist(c,data):
    name=data.split(' ')[1]
    r=db.history(name)
    if not r:
        c.send(b"Fail")
        return
    c.send(b"OK")

    for i in r:
        msg='%s %-16s %s'%i
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b"##")

def do_register(c,data):
    tmp=data.split(' ')
    name=tmp[1]
    passwd=tmp[2]
    if db.register(name,passwd):
        c.send(b"OK")
    else:
        c.send(b"Fail")

def do_login(c,data):
    tmp=data.split(' ')
    name=tmp[1]
    passwd=tmp[2]
    if db.login(name,passwd):
        c.send(b"OK")
    else:
        c.send(b"False")

# 接收客户端请求,分配处理函数
def request(c):
    db.create_cursor()
    while True:
        data=c.recv(1024).decode()
        print(c.getpeername(),':',data)
        if not data or data[0]=='E':
            sys.exit() # 对应子进程退出
        elif data[0]=='R':
            do_register(c,data)
        elif data[0]=='L':
            do_login(c,data)
        elif data[0]=='Q':
            do_query(c,data)
        elif data[0]=='H':
            do_hist(c,data)

def main():
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    # 循环等待客户端连接
    print('Listen the port 8888')
    while True:
        try:
            c,addr=s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            s.close()
            db.close()
            sys.exit("服务端退出")
        except Exception as e:
            print(e)
            continue

        p=Process(target=request,args=(c,))
        p.daemon=True
        p.start()

if __name__=='__main__':
    main()


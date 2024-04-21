from socket import *
import os,sys

ADDR=('0.0.0.0',8888)
user={}

def do_login(s,name,addr):
    if name in user or '管理员' in name:
        s.sendto('该用户存在'.encode(),addr)
        return
    s.sendto(b'OK',addr) # 可以进入聊天室
    # 通知其他人
    msg='\n欢迎"%s"进入聊天室'%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    # 存储用户
    user[name]=addr

def do_chat(s,name,text):
    msg='\n%s: %s'%(name,text)
    for i in user:
        if i!=name:
            s.sendto(msg.encode(),user[i])

def do_quit(s,name):
    msg='\n%s 退出聊天室'%name
    for i in user:
        if i!=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    del user[name]

def do_request(s):
    while True:
        data,addr=s.recvfrom(1024)
        tmp=data.decode().split(' ')
        # 根据不同的请求类型具体执行不同的事情
        #L 进入     C 聊天  Q 退出
        if tmp[0]=='L':
            do_login(s,tmp[1],addr)
        elif tmp[0]=='C':
            text=' '.join(tmp[2:])
            do_chat(s,tmp[1],text)
        elif tmp[0]=='Q':
            do_quit(s,tmp[1])

def main():
    s=socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid=os.fork()
    if pid==0:
        while True:
            msg=input('管理员消息:')
            msg='C 管理员 '+msg
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s)

main()

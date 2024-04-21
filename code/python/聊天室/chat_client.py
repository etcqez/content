from socket import *
import os,sys

ADDR=('0.0.0.0',8888)

# 发送消息
def send_msg(s,name):
    while True:
        try:
            text=input('发言:')
        except KeyboardInterrupt:
            text='quit'
        if text.strip()=='quit':
            msg='Q '+name
            s.sendto(msg.encode(),ADDR)
            sys.exit('退出聊天室')
        msg='C %s %s'%(name,text)
        s.sendto(msg.encode(),ADDR)

def recv_msg(s):
    while True:
        try:
            data,addr=s.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        if data.decode()=='EXIT':
            sys.exit()
        print(data.decode()+'\n发言:',end='')

def main():
    s=socket(AF_INET,SOCK_DGRAM)
    
    # 进入聊天室
    while True:
        name=input('请输入姓名:')
        msg='L '+name
        s.sendto(msg.encode(),ADDR)
        data,addr=s.recvfrom(128)
        if data.decode()=='OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())

    # 已经进入聊天室
    pid=os.fork()
    if pid<0:
        sys.exit('Error!')
    elif pid==0:
        send_msg(s,name) # 子进程负责消息发送
    else:
        recv_msg(s) # 父进程负责消息接收

main()

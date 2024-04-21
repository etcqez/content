import socket

sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sockfd.connect(('127.0.0.1',8888))

# 发送
data=input('Msg>>')
sockfd.send(data.encode())
data=sockfd.recv(1024)
print("Server:",data.decode())

sockfd.close()


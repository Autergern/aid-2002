from socket import *
from threading import Thread
import sys
import os
from time import sleep

# 服务器地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
FTP = '/home/tarena/wh/'


class FTPServer(Thread):
    def __init__(self, connfd):
        super().__init__()
        self.connfd = connfd

    def do_list(self):
        file_list = os.listdir(FTP)
        if not file_list:
            self.connfd.send(b'NO')
            return
        else:
            self.connfd.send(b'YES')
            sleep(0.1)
            data = '\n'.join(file_list)
            self.connfd.send(data.encode())

    def do_get(self, filename):
        try:
            f = open(FTP+filename, 'rb')
        except:
            self.connfd.send(b'NO')
            return
        else:
            self.connfd.send(b'YES')
            sleep(0.1)
            while True:
                data = f.read(1024)
                if not data:
                    sleep(0.1)
                    self.connfd.send(b'##')
                    break
                self.connfd.send(data)
            f.close()

    def do_put(self, filename):
        if os.path.exists(FTP + filename):
            self.connfd.send(b'NO')
            return
        else:
            self.connfd.send(b'YES')
            f = open(FTP + filename, 'wb')
            while True:
                data = self.connfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()

    def run(self):
        while True:
            data = self.connfd.recv(1024).decode()
            if not data or data == 'E':
                return
            elif data == 'L':
                self.do_list()
            elif data[0] == 'G':
                filename = data.split(' ')[-1]
                self.do_get(filename)
            elif data[0] == 'P':
                filename = data.split(' ')[-1]
                self.do_put(filename)


def main():
    # 创建套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(3)
    print('Listen the port 8888')

    # 循环连接客户端
    while True:
        try:
            connfd, addr = sock.accept()
            print("客户端地址:", addr)
        except:
            sys.exit('服务退出')

        # 创建子进程,处理客户端请求
        t = FTPServer(connfd)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
##
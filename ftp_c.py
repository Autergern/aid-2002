from socket import *
import time
import sys

ADDR = ('127.0.0.1', 8888)


class FTPClient:
    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b'L')
        data = self.sockfd.recv(128).decode()
        if data == 'YES':
            data = self.sockfd.recv(4096)
            print(data.decode())
        else:
            print('获取文件列表失败')

    def do_get(self, filename):
        data = 'G ' + filename
        # print(data)
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(128).decode()
        if data == 'YES':
            f = open(filename, 'wb')
            while True:
                data = self.sockfd.recv(1024)
                if data == b'##':
                    break
                f.write(data)
            f.close()
        else:
            print('没有这个文件')

    def do_put(self, filename):
        try:
            f = open(filename, 'rb')
        except:
            print('要上传得文件不存在')
            return
        filename = filename.split('/')[-1]
        data = 'P ' + filename
        self.sockfd.send(data.encode())
        data = self.sockfd.recv(128).decode()
        if data == 'YES':
            while True:
                data = f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.sockfd.send(b'##')
                    break
                self.sockfd.send(data)
            f.close()
        else:
            print('文件已存在')

    def do_quit(self):
        self.sockfd.send(b'E')
        self.sockfd.close()
        sys.exit('谢谢使用')


def main():
    s = socket()
    s.connect(ADDR)

    ftp = FTPClient(s)

    while True:
        print('命令选项:')
        print('list')
        print('get file')
        print('put file')
        print('quit')
        print('=============================')

        cmd = input("请输入命令:")
        if cmd == 'list':
            ftp.do_list()
        elif cmd[:3] == 'get':
            filename = cmd.split(' ')[-1]
            # print(filename)
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.split(' ')[-1]
            ftp.do_put(filename)
        elif cmd == 'quit':
            ftp.do_quit()
        else:
            print('请输入正确命令')


if __name__ == '__main__':
    main()

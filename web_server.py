from socket import *
from select import select
import re


# 主体功能
class HTTPServer:
    def __init__(self, host='0.0.0.0', port=80, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setblocking(False)

    def bind(self):
        self.address = (self.host, self.port)
        self.sockfd.bind(self.address)

    def start(self):
        self.sockfd.listen(3)
        print('Listen the port %s' % self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c, addr = r.accept()
                    print("Connect from", addr)
                    c.setblocking(False)
                    self.rlist.append(c)
                else:
                    self.handle(r)

    def handle(self, connfd):
        request = connfd.recv(1024).decode()
        # print(request)
        pattern = r'[A-Z]+\s+(/\S*)'
        try:
            info = re.match(pattern, request).group(1)
        except:
            self.rlist.remove(connfd)
            connfd.close()
            return
        # print(info)
        else:
            self.get_html(connfd, info)

    def get_html(self, connfd, info):
        if info == '/':
            filename = self.html + '/index.html'
        else:
            filename = self.html + info
        try:
            f = open(filename, 'rb')
        except:
            response_headers = 'HTTP/1.1 404 NOT FOUND\r\n'
            response_headers += 'Content_Type:text/html\r\n'
            response_headers += '\r\n'
            response_content = '<h1>Sorry......</h1>'
            response = (response_headers + response_content).encode()
        else:
            response_content = f.read()
            response_headers = 'HTTP/1.1 200 OK\r\n'
            response_headers += 'Content_Type:text/html\r\n'
            response_headers += 'Content_Length:%d\r\n' % len(response_content)
            response_headers += '\r\n'
            response = response_headers.encode() + response_content
        finally:
            connfd.send(response)


if __name__ == '__main__':
    """
    通过HTTPServer类快速搭建服务
    static中有一组网页,展示这组网页
    """
    # 需要使用者提供:网络地址  网页位置
    host = '0.0.0.0'
    port = 8001
    dir = '../stage2/day17/static'
    # 实例化对象
    httpd = HTTPServer(host=host, port=port, html=dir)
    # 调用方法启动服务
    httpd.start()

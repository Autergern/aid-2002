from socket import *
from time import ctime, sleep

f = open('net.log', 'a+')

sockfd = socket()
sockfd.bind(('127.0.0.1', 8888))
sockfd.listen(3)

# sockfd.setblocking(False)

sockfd.settimeout(2)

while True:
    print('Waiting for connect...')
    try:
        connfd, addr = sockfd.accept()
        print('connect from', addr)
    except timeout as e:
        sleep(2)
        f.write('%s:%s\n' % (ctime(), e))
        f.flush()
    except BlockingIOError as e:
        sleep(2)
        f.write('%s:%s\n' % (ctime(), e))
        f.flush()
    else:
        data = connfd.recv(1024)
        print(data)

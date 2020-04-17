"""
屏蔽功能
"""
from socket import *
from multiprocessing import Process
import re


HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)
user = {}


def do_login(s, name, address):
    if name in user or "管理" in name:
        s.sendto("该用名已经存在".encode(), address)
        return
    else:
        s.sendto(b'OK', address)
        msg = "\n欢迎 %s 进入聊天室" % name
        for i in user:
            s.sendto(msg.encode(), user[i])
        user[name] = address


def do_chat(s, name, text):
    msg = "%s : %s" % (name, text)
    dict_shield = {}
    list_words = ['xx', 'aa', 'bb', 'oo']
    pattern = r'[aoxb]{2}'
    words = re.findall(pattern, text)
    if name not in dict_shield:
        for word in words:
            if word in list_words:
                s.sendto('该条消息含敏感词汇'.encode(), user[name])
                dict_shield[name] = 1
                for i in user:
                    if i != name:
                        s.sendto(('%s被禁言' % name).encode(), user[i])
            else:
                for i in user:
                    if i != name:
                        s.sendto(msg.encode(), user[i])
            break
    elif name in dict_shield:
        for word in list_words:
            if word in words:
                s.sendto('该条消息含敏感词汇'.encode(), user[name])
                dict_shield[name] += 1
            else:
                if dict_shield[name] == 3:
                    s.sendto('你已被提出群聊'.encode(), user[name])
                    del dict_shield[name]
                    del user[name]
                else:
                    for i in user:
                        if i != name:
                            s.sendto(msg.encode(), user[i])


def do_quit(s, name):
    del user[name]
    msg = "\n%s 退出聊天室" % name
    for i in user:
        s.sendto(msg.encode(), user[i])


def request(s):
    while True:
        data, addr = s.recvfrom(1024)
        tmp = data.decode().split(' ', 2)
        if tmp[0] == 'L':
            do_login(s, tmp[1], addr)
        elif tmp[0] == 'C':
            do_chat(s, tmp[1], tmp[2])
        elif tmp[0] == 'Q':
            do_quit(s, tmp[1])


def manager(s):
    while True:
        msg = input("管理员消息:")
        msg = "C 管理员 " + msg
        s.sendto(msg.encode(), ADDR)


def main():
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind(ADDR)
    p = Process(target=request, args=(s,))
    p.start()
    manager(s)
    p.join()


if __name__ == '__main__':
    main()

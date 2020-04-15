from socket import *

sockfd = socket()
sockfd.bind(('0.0.0.0', 8888))
sockfd.listen(3)

c, addr = sockfd.accept()
print('Connect from', addr)

data = c.recv(2048)
print(data.decode())

http_data = '''HTTP/1.1 200 OK
Content_Type:text/html

Hello World!
'''

c.send(http_data.encode())

c.close()
sockfd.close()

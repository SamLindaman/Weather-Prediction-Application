#pythonSocket Client

from socket import *

host = input('Input IP: ')
if not host:
    host = '' #oriented object

port = int(input('Input Port Number: ')) # Port number must be int. so change to int
if not port:
    port = 1999

HOST = host
PORT = port
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM) # make a client socket
tcpCliSock.connect(ADDR) # Request to connect the server (ADDR)

while True:
    data = input('> ')
    if not data:
        break

    tcpCliSock.send(bytes(data, 'utf-8')) # input data send to the Server
    data = tcpCliSock.recv(BUFSIZ) # recieve the data from the server
    if not data:
        break
    print(data) # data output

tcpCliSock.close()

#pythonSocket server

from socket import * #for socket communication
from time import * # for print out for time

HOST = ''
PORT = 1999 # you want to set the number feel free.
ADDR = (HOST, PORT) #means address. must be paired with the host (IP) and port number.
BUFSIZ = 1024 #recieved message size

# The part that creates the socket. AF_INET stands for network and SOCK_STEM stands for TCP.
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR) # Insert the specified address (ADDR) into the socket you created.
tcpSerSock.listen(5) # Listen means the maximum number of connections that can be accepted before a denial.


while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ) #recv()is the function which is recieved the other client socket. (in using udp, they are also different)
        if not data:
            break
        tcpCliSock.send(bytes('[%s] %s' % (ctime(), data), 'utf-8'))

    tcpCliSock.close() # shut down the server
tcpSerSock.close()

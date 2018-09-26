# python 3.6.4
# COMP9331 Lab3
# Xiaodan Wang z5145114

from socket import *
from os import path
from os import listdir
import sys
# get the port num
serverPort = str(sys.argv[1])
# establish TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', int(serverPort)))
serverSocket.listen(1)
print("The server is ready to receive")

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    # get requst file name
    a = sentence.decode()
    if not a:
        continue
    s = a.split('\r\n')
    src = s[0].split(' ')
    filename = src[1][1:]

    # response
    dirlist = listdir()
    # file not found
    if filename not in set(dirlist):
        with open('notfound.html') as notfoundfile:
            notfound = notfoundfile.read()
        message = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n\r\n'+notfound
        b = message.encode()
        connectionSocket.sendall(b) 
    # file found
    else:                  
        # html
        if filename.split('.')[1] == 'html':
            with open(filename,'r') as file:
                content = file.read()
            print(content)            
            message = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'+content
            b = message.encode()
            connectionSocket.sendall(b)
            continue
        # png
        elif filename.split('.')[1] == 'png':
            with open(filename,'rb') as file:
                content = file.read()
            message = 'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n'
            print('pngmessage')
            b = message.encode() + content
            connectionSocket.sendall(b)
            continue        
        else:
            continue        
    connectionSocket.close()


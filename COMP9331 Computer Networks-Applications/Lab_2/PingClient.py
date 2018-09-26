# python 3.6.4
# COMP9331 Lab2
# Xiaodan Wang z5145114

import sys
import time
from socket import *
from numpy import mean
    
# host and port
serverName = str(sys.argv[1])
serverPort = str(sys.argv[2])
# establish client socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
# timeout 1 second wait
clientSocket.settimeout(1)

# min, max, avg
rtt = []

# 10 ping requests
for sequence in range(10):
    # massage sent: PING sequence_number timestamp
    timestamp = int(round(time.time() * 1000))
    massage1 = 'PING'+' '+str(sequence)+' '+str(timestamp)
    clientSocket.sendto(massage1.encode(),(serverName, int(serverPort)))
    #print(f'send:{massage1} to {serverName},{serverPort}')

    # massage recieved: PING sequence_number timestamp CRLF
    try:
        # massage recieved
        recieved = clientSocket.recv(20)
        timerecv = int(round(time.time() * 1000))
        massage2 = recieved.decode()
        a  = massage2.split()
        print(a)
        print(f'pint to {serverName}, seq = {a[1]}, rtt = {timerecv-int(a[2])} ms')
        rtt.append(timerecv-int(a[2]))
        
    # time out
    except:
        print(f'pint to {serverName}, seq = {sequence}, time out')
        continue

if rtt:
    print(f'min rtt: {min(rtt)}\nmax rtt: {max(rtt)}\navg rtt: {int(mean(rtt))}')
else:
    print('min rtt: None\nmax rtt: None\navg rtt: None')
print(f'loss rate: {(10 - len(rtt))/10}')

clientSocket.close()

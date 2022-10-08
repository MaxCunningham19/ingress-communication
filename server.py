# based on https://pythontic.com/modules/socket/udp-client-server-example
from statistics import mean
from typing import List
import socket
import constants as cons
from encode import encode
from encode import decode
import server_worker as swork

localIP     = "pserver" #socket.gethostbyname(socket.gethostname())
localPort   = 50000
bufferSize  = 1024

msgFromServer       = "Hello From Server"

workers: List[swork.Worker] = []

def select_worker(workers:List[swork.Worker])->int:
    for i in range(workers):
        if not workers[i].isBusy():
            return i
    return -1

def get_worker(workers:List[swork.Worker],address:tuple(str,int))->int:
    for i in range(workers):
        if workers[i].isAddress(address):
            return i
    return -1

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening @", UDPServerSocket.getsockname())


# Listen for incoming datagrams
while(True):        
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    origAddress, input, message = decode(message)

    if message is not None:
        if cons.isAddWorker(input):
            workerMsg = "Adding Worker "+address[0]+" : "+str(address[1])
            print(workerMsg)
            workers.append(swork.Worker(address,False))
            UDPServerSocket.sendto(encode(origAddress,message,cons.ACK),address)
        elif cons.isGet(input):
            index = select_worker(workers)
            if index == -1:
                UDPServerSocket.sendto(encode(origAddress,message,cons.BUSY),address)
            else:
                UDPServerSocket.sendto(encode(origAddress,message,cons.GET),workers[index].address)
        elif cons.isResp(input):
            index = get_worker(workers,address)
            if index == -1:
                UDPServerSocket.sendto(encode(origAddress,message,cons.REJ),address)
            else:
                UDPServerSocket.sendto(encode(address,message,cons.RESP),origAddress)
        elif cons.isACK(input):
            index = get_worker(workers,address)
            if index == -1:
                UDPServerSocket.sendto(encode(address,message,cons.ACK),origAddress)
            else:
                UDPServerSocket.sendto(encode(address,message,cons.ACK),origAddress)
        else:
            print(input, "cannot be handled by the sever")
            UDPServerSocket.sendto(encode(origAddress,message,cons.REJ),address)
    else:
        print("cannot handle address or port given in incorrect form\n")


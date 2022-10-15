# based on https://pythontic.com/modules/socket/udp-client-server-example
from typing import List
import socket
import time
import constants as cons
from encode import encode
from encode import decode
import server_worker as swork

localIP     = "pserver"
localPort   = 50000
bufferSize  = 1024


msgFromServer  = "Hello From Server"
workers: List[swork.Worker] = []

def recieve(UDPSocket: socket.socket):
    print("waiting to recieve messages")
    while True:
        try:
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            origAddress, input, message = decode(message)
            return origAddress, input, message, address
        except:
            continue


def add_worker(workers:List[swork.Worker],address)->bool:
    for i in range(len(workers)):
        if workers[i].isAddress(address):
            return False
    return True

def select_worker(workers:List[swork.Worker])->int:
    for i in range(len(workers)):
        if not workers[i].isBusy():
            return i
    return -1

def get_worker(workers:List[swork.Worker],address)->int:
    for i in range(len(workers)):
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
    origAddress, input, message, address = recieve(UDPServerSocket)
    origAddress = (socket.gethostbyname(origAddress[0]),origAddress[1])
    if message is not None:
        if cons.isAddWorker(input):
            if add_worker(workers, address):
                workers.append(swork.Worker(address,False))
                workerMsg = "Adding Worker "+address[0]+" : "+str(address[1])
                print(workerMsg)
            time.sleep(2)
            message = encode(origAddress, message,cons.ACK)
            UDPServerSocket.sendto(message , origAddress)
            print("sent ACK to worker @", origAddress)
        elif cons.isGet(input):
            index = select_worker(workers)
            if index == -1:
                UDPServerSocket.sendto(encode(origAddress,message,cons.BUSY),address)
            else:
                UDPServerSocket.sendto(encode(origAddress,message,cons.GET),workers[index].address)
                workers[index].busy = True
        elif cons.isResp(input):
            UDPServerSocket.sendto(encode(address,message,cons.RESP),origAddress)
        elif cons.isACK(input):
            index = get_worker(workers,address)
            if index != -1 :
                workers[index].busy = False
            UDPServerSocket.sendto(encode(address,message,cons.ACK),origAddress)
        else:
            print(input, "cannot be handled by the sever")
            UDPServerSocket.sendto(encode(origAddress,message,cons.REJ),address)
    else:
        print("cannot handle address or port given in incorrect form")


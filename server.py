# based on https://pythontic.com/modules/socket/udp-client-server-example
from typing import List
import socket
import time
import constants as cons
from encode import encode
from encode import decode
import server_worker as swork

localIP = "server"
localPort = 50000
bufferSize = 1024


msgFromServer = "Hello From Server"
workers: List[swork.Worker] = []


def recieve(UDPSocket: socket.socket):
    while True:
        try:
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            origAddress, input, message, num = decode(message)
            return origAddress, input, message, num, address
        except TimeoutError:
            continue


def add_worker(workers: List[swork.Worker], address) -> bool:
    for i in range(len(workers)):
        if workers[i].isAddress(address):
            return False
    return True


def select_worker(workers: List[swork.Worker]) -> int:
    for i in range(len(workers)):
        if not workers[i].isBusy():
            return i
    return -1


def get_worker(workers: List[swork.Worker], address) -> int:
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
while (True):
    origAddress, input, message, num, address = recieve(UDPServerSocket)
    origAddress = (socket.gethostbyname(origAddress[0]), origAddress[1])
    if message is not None:
        if cons.isAddWorker(input):
            if add_worker(workers, address):
                workers.append(swork.Worker(address, False))
                workerMsg = "Adding Worker " + \
                    address[0] + " : " + str(address[1])
                print(workerMsg)
            message = encode(origAddress, message, cons.ACK, num)
            UDPServerSocket.sendto(message, origAddress)
        elif cons.isGet(input):
            index = select_worker(workers)
            if index == -1:
                UDPServerSocket.sendto(
                    encode(origAddress, message, cons.BUSY, num), address)
            else:
                print("establishing connection between",
                      workers[index].address, "and", address)
                UDPServerSocket.sendto(
                    encode(origAddress, message, cons.GET, num), workers[index].address)
                workers[index].busy = True
        elif cons.isResp(input):
            UDPServerSocket.sendto(
                encode(address, message, cons.RESP, num), origAddress)
        elif cons.isACK(input) or cons.isRej(input):
            index = get_worker(workers, address)
            if index != -1:
                workers[index].busy = False
                print("closing connection between",
                      workers[index].address, "and", origAddress)
            UDPServerSocket.sendto(
                encode(address, message, input, num), origAddress)
    else:
        print("cannot handle recieved message")

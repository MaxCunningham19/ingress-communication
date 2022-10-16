# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from encode import decode
from encode import encode
import constants as cons


def connect(UDPWorkerSocket: socket.socket, worker_adrs):
    msg = encode(worker_adrs, b'0', cons.WORKER,0)
    while True:
        UDPWorkerSocket.sendto(msg, server_address)
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            origAddress, operation, _ , _ = decode(bytesAddressPair[0])
            if origAddress is not None:
                if cons.isACK(operation):
                    return
        except TimeoutError:
            continue


def recieve(UDPWorkerSocket: socket.socket):
    print("waiting to recieve messages")
    while True:
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            origAddress, input, msg, num = decode(message)
            return origAddress, input, msg, num, address
        except TimeoutError:
            continue


def split(msg:str|bytes):

    ThrdLen = int(len(msg)/3)
    msg_arr = [msg[:ThrdLen],msg[ThrdLen:ThrdLen*2],msg[ThrdLen*2:]]
    return msg_arr

def respond(UDPWorkerSocket: socket.socket, origAddress, msg:str|bytes):    
    response = split(msg)
    for i in range(len(response)):
        sending = encode(origAddress, response[i], cons.RESP, i)
        while True:
            try:
                UDPWorkerSocket.sendto(sending, server_address)
                bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
                origAdrs, oper, mes, num = decode(bytesAddressPair[0])
                print(origAdrs, oper, mes, num)
                if origAdrs is not None:
                    if cons.isACK(oper) and num == i:
                        break
            except TimeoutError:
                continue

    sending = encode(origAddress, "", cons.ACK, len(response))
    while True:
        try:
            UDPWorkerSocket.sendto(sending, server_address)
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            origAdrs, oper, mes, num = decode(bytesAddressPair[0])
            print(origAdrs, oper, mes, num)
            if origAdrs is not None:
                if cons.isACK(oper) and num==len(response):
                    return
        except TimeoutError:
            continue



dockername = input("docker container name: ")

server_address = ("pserver", 50000)
bufferSize = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((dockername, 0))
UDPWorkerSocket.settimeout(3.0)
print("Worker starting @ ", dockername, UDPWorkerSocket.getsockname()[1])
worker_adrs = (UDPWorkerSocket.getsockname())

# connect to server
connect(UDPWorkerSocket, worker_adrs)
print("connected to server")

# Listen for incoming datagrams
while (True):
    try:
        origAddress, op, message, num, address = recieve(UDPWorkerSocket)
        print(origAddress, op, message, address)
        if origAddress is not None and cons.isGet(op):
            respond(UDPWorkerSocket, origAddress, message)
        else:
            print("worker recived invalid message")
            msg = encode(origAddress, message, cons.REJ, num)
            UDPWorkerSocket.sendto(msg, address)
    except TimeoutError:
        continue

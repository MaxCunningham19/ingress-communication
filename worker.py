# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from unittest import skip
from encode import decode
from encode import encode
import constants as cons


def connect(UDPWorkerSocket: socket.socket, worker_adrs):
    msg = encode(worker_adrs, b'0', cons.WORKER)
    while True:
        UDPWorkerSocket.sendto(msg, server_address)
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            origAddress, operation, message = decode(bytesAddressPair[0])
            if origAddress is not None:
                if cons.isACK(operation):
                    return
        except:
            continue


def recieve(UDPWorkerSocket: socket.socket):
    while True:
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            return decode(message), address
        except:
            continue


def send(UDPWorkerSocket: socket.socket, origAddress, message:str|bytes, op:str):
    while True:
        try:
            message = encode(origAddress, message, op)
            print("worker sending", message, "to server")
            UDPWorkerSocket.sendto(message, address)
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            origAddress, operation, message = decode(bytesAddressPair[0])
            if origAddress is not None:
                if cons.isACK(operation):
                    return
        except:
            continue


dockername = input("docker container name: ")

server_address = ("pserver", 50000)
bufferSize = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((dockername, 0))
UDPWorkerSocket.settimeout(2.0)
print("Worker starting @ ", dockername, UDPWorkerSocket.getsockname()[1])
worker_adrs = (UDPWorkerSocket.getsockname())

# connect to server
connect(UDPWorkerSocket, worker_adrs)


# Listen for incoming datagrams
while (True):
    try:
        origAddress, op, message, address = recieve(UDPWorkerSocket)
        if origAddress is not None and cons.isGet(op):
            send(UDPWorkerSocket,worker_adrs,"hey",cons.RESP)
        else:
            print("worker recived invalid message")
            encode(origAddress, message, cons.REJ)
            UDPWorkerSocket.sendto(message, address)
    except:
        continue

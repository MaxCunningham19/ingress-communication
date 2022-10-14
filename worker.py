# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from encode import decode
from encode import encode
import constants as cons


def connect(UDPWorkerSocket: socket.socket, worker_adrs):
    msg = encode(worker_adrs, b'0', cons.WORKER)
    while True:
        UDPWorkerSocket.sendto(msg, server_address)
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            origAddress, operation, _ = decode(bytesAddressPair[0])
            if origAddress is not None:
                if cons.isACK(operation):
                    return
        except:
            continue


def recieve(UDPWorkerSocket: socket.socket):
    print("waiting to recieve messages")
    while True:
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            origAddress, input, msg = decode(message)
            return origAddress, input, msg, address
        except:
            continue


def send(UDPWorkerSocket: socket.socket, origAddress, msg:str|bytes, op:str):
    while True:
        try:
            sending = encode(origAddress, msg, op)
            print("worker sending", sending, "to server")
            UDPWorkerSocket.sendto(sending, server_address)
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            origAdrs, oper, _ = decode(bytesAddressPair[0])
            if origAdrs is not None:
                if cons.isACK(oper):
                    return
        except:
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
        origAddress, op, message, address = recieve(UDPWorkerSocket)
        if origAddress is not None and cons.isGet(op):
            send(UDPWorkerSocket,origAddress,"hey",cons.RESP)
        else:
            print("worker recived invalid message")
            encode(origAddress, message, cons.REJ)
            UDPWorkerSocket.sendto(message, address)
    except:
        continue

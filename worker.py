# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from typing import List
from encode import decode
from encode import encode
from worker_util import split, getFile
import constants as cons


def connect(UDPWorkerSocket: socket.socket):
    msg = encode(b'0', cons.WORKER, 0)
    while True:
        UDPWorkerSocket.sendto(msg, server_address)
        try:
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            operation, _, _ = decode(bytesAddressPair[0])
            if operation is not None:
                if cons.isACK(operation):
                    return
        except TimeoutError:
            continue


def send_done(UDPWorkerSocket: socket.socket):
    msg = encode(b'0', cons.DONE, 0)
    while True:
        try:
            UDPWorkerSocket.sendto(msg, server_address)
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            operation, _, _ = decode(bytesAddressPair[0])
            if operation is not None:
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
            input, num, msg = decode(message)
            return input, msg, num, address
        except TimeoutError:
            continue


def respond(UDPWorkerSocket: socket.socket, msg: str | bytes):
    response = split(cons.MAX_MSG_LENGTH, msg)
    for i in range(len(response)):
        sending = encode(response[i], cons.RESP, i)
        while True:
            try:
                UDPWorkerSocket.sendto(sending, server_address)
                bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
                oper, num, _ = decode(bytesAddressPair[0])
                print(oper, num)
                if oper is not None:
                    if cons.isACK(oper) and num == (i % 16):
                        break
            except TimeoutError:
                continue

    sending = encode("", cons.ACK, len(response))
    while True:
        try:
            UDPWorkerSocket.sendto(sending, server_address)
            bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
            oper, num, _ = decode(bytesAddressPair[0])
            print(oper, num)
            if oper is not None:
                if cons.isACK(oper) and num == len(response) % 16:
                    send_done(UDPWorkerSocket)
                    return
        except TimeoutError:
            continue


dockername = input("docker container name: ")

server_address = ("server", 50000)
bufferSize = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((dockername, 0))
UDPWorkerSocket.settimeout(3.0)
print("Worker starting @ ", UDPWorkerSocket.getsockname())
worker_adrs = (UDPWorkerSocket.getsockname())

# connect to server
connect(UDPWorkerSocket)
print("connected to server")

# Listen for incoming datagrams
while (True):
    try:
        op, message, num, address = recieve(UDPWorkerSocket)
        print(op, message, address)
        if op is not None and cons.isGet(op):
            filename = message.decode()
            content = getFile(filename)
            if content == b'':
                print("file", filename, "cannot be opened")
                msg = encode(b'', cons.REJ, 0)
                UDPWorkerSocket.sendto(msg, server_address)
                send_done(UDPWorkerSocket)
            else:
                respond(UDPWorkerSocket, content)

        else:
            print("worker recived invalid message")
            msg = encode(message, cons.REJ, num)
            UDPWorkerSocket.sendto(msg, address)

    except TimeoutError:
        continue

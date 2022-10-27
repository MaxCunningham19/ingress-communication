# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
import time as time
from typing import List
import constants as cons
from encode import encode
from encode import decode


def send(UDPSocket: socket.socket, message_p: bytes,):
    response: List[bytes] = []
    curNum = 0
    while True:
        try:
            msg = encode(message_p, cons.GET, curNum)
            UDPSocket.sendto(msg, server_address)

            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            operation, num, resp_msg = decode(bytesAddressPair[0])
            if operation is not None:
                if cons.isRej(operation):
                    return b''
                if cons.isResp(operation):
                    if curNum == num:
                        print(operation, num)
                        response.append(resp_msg)
                        curNum = (curNum + 1) % 16
                        msg = encode('', cons.ACK, num)
                        UDPSocket.sendto(msg, server_address)
                        break
                if cons.isBusy(operation):
                    print("server is busy client waiting...")
                    time.sleep(2)

        except TimeoutError:
            continue

    while True:
        try:
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            operation, num, resp_msg = decode(bytesAddressPair[0])
            if operation is not None:
                print(operation, num)
                if cons.isACK(operation):
                    msg = encode('', cons.ACK, num)
                    UDPSocket.sendto(msg, server_address)
                    res = bytes.join(b'', response)
                    return res
                if cons.isResp(operation):
                    if curNum == num:
                        response.append(resp_msg)
                        curNum = (curNum + 1) % 16
                    if (num+1) % 16 > curNum:
                        return "error client worker connection broke"
                    else:
                        msg = encode(resp_msg, cons.ACK, num)
                        UDPSocket.sendto(msg, server_address)
        except TimeoutError:
            continue


server_address = ("server", 50000)
bufferSize = 1024

dockername = input("docker container name: ")

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind((dockername, 0))
print(UDPClientSocket.getsockname())
UDPClientSocket.settimeout(3.0)

while True:
    filePath = input("what is the file you wish to recieve: ")

    # Send to server using created UDP socket
    print("sending to server @", server_address)
    res = send(UDPClientSocket, filePath)

    if res != b'':
        print("recieved ack writing to", "client_"+filePath)
        file = open("client_"+filePath, 'wb')
        file.write(res)
        file.close()
        startTime = time.time()
        while True:
            try:
                bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
                operation, num, resp_msg = decode(bytesAddressPair[0])
                print(operation, resp_msg, num)
                if operation is not None:
                    if cons.isACK(operation):
                        msg = encode(resp_msg, cons.ACK, num)
                        UDPClientSocket.sendto(msg, server_address)
            except TimeoutError:
                if time.time() - startTime > 5:
                    break
    else:
        print("message rejected by server")

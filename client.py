# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
import time as time
from typing import List
import constants as cons
from encode import encode
from encode import decode


def recieve(UDPSocket: socket.socket):
    print("waiting to recieve messages")
    while True:
        try:
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            byte_message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            origAddress, input, message_decoded = decode(byte_message)
            return origAddress, input, message_decoded, address
        except TimeoutError:
            continue


def send(UDPSocket: socket.socket, origAddress, message_p: bytes,):
    response: List[bytes] = []
    curNum = 0
    while True:
        try:
            msg = encode(origAddress, message_p, cons.GET, curNum)
            UDPSocket.sendto(msg, server_address)

            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            origAddress, operation, resp_msg, num = decode(bytesAddressPair[0])
            if origAddress is not None:
                if cons.isRej(operation):
                    return b''
                if cons.isResp(operation):
                    if curNum == num:
                        print(origAddress, operation, num)
                        response.append(resp_msg)
                        curNum = (curNum + 1) % 16
                        msg = encode(origAddress, '', cons.ACK, num)
                        UDPSocket.sendto(msg, server_address)
                        break
                if cons.isBusy(operation):
                    time.sleep(2)

        except TimeoutError:
            continue

    while True:
        try:
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            origAddress, operation, resp_msg, num = decode(bytesAddressPair[0])
            if origAddress is not None:
                print(origAddress, operation, num)
                if cons.isACK(operation):
                    msg = encode(origAddress, '', cons.ACK, num)
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
                        msg = encode(origAddress, resp_msg, cons.ACK, num)
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
    res = send(UDPClientSocket, UDPClientSocket.getsockname(), filePath)

    if res != b'':
        print("recieved ack writing to", "client_"+filePath)
        file = open("client_"+filePath, 'wb')
        file.write(res)
        file.close()
        startTime = time.time()
        while True:
            try:
                bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
                origAddress, operation, resp_msg, num = decode(bytesAddressPair[0])
                print(origAddress, operation, resp_msg, num)
                if origAddress is not None:
                    if cons.isACK(operation):
                        msg = encode(origAddress, resp_msg, cons.ACK, num)
                        UDPClientSocket.sendto(msg, server_address)
            except TimeoutError:
                if time.time() - startTime > 5:
                    break
    else:
        print("message rejected by server")

# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
import constants as cons
from encode import encode
from encode import decode

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


def send(UDPSocket: socket.socket, origAddress, message:str|bytes, op:str):
    while True:
        try:
            message = encode(origAddress, message, op)
            print("client sending", message, "to server")
            UDPSocket.sendto(message, server_address)
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            origAddress, operation, message = decode(bytesAddressPair[0])
            if origAddress is not None:
                if cons.isACK(operation):
                    return
        except:
            continue

msgFromClient       = "filename.txt"
server_address   = ("pserver", 50000)
bufferSize          = 1024

localIP     = "pclient"

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind((localIP,0))
print(UDPClientSocket.getsockname())
UDPClientSocket.settimeout(3.0)

# Send to server using created UDP socket
print("sending to server @",server_address)
send(UDPClientSocket, UDPClientSocket.getsockname(),msgFromClient,cons.GET)

origAddress, op, message, address = recieve(UDPClientSocket)
print(origAddress, op, message, address)
send(UDPClientSocket, UDPClientSocket.getsockname(),msgFromClient,cons.ACK)

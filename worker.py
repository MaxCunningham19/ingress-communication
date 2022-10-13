# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from unittest import skip
from encode import decode
from encode import encode
import constants as cons

dockername = input("docker container name:")

server_address = ("pserver",50000)
bufferSize  = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPWorkerSocket.bind((dockername,0))
UDPWorkerSocket.settimeout(2.0)

print("Worker starting @ ",dockername,UDPWorkerSocket.getsockname()[1])
worker_adrs = (socket.gethostname(),UDPWorkerSocket.getsockname()[1])

msg = encode(False,worker_adrs,b'0',cons.WORKER)
UDPWorkerSocket.sendto(msg,server_address) 

# connect to server
connecting = True
while connecting:
    UDPWorkerSocket.sendto(msg,server_address)
    try:
        bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
        hasAdrs, origAddress, operation, message = decode(bytesAddressPair[0])
        if origAddress is not None:
            if cons.isACK(operation):
                print("UDP worker @",UDPWorkerSocket.getsockname(),"connected to server @",bytesAddressPair[1])
                connecting = False
    except TimeoutError:
        print("resending handshake message")


# Listen for incoming datagrams
while(True):
    try:
        bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        serverMsg = "Message from Server:{}".format(message)
        serverIP  = "Server IP Address:{}".format(address)
        print(serverMsg)
        print(serverIP)

        hasAddress, destAddress,input, message = decode(message)
        if destAddress is not None and hasAddress is True:
            clientIP = "Client Ip Address:{}".format(destAddress)
            print(clientIP, message, input)

            message = encode(True,destAddress, message,cons.RESP)
            print("worker sending",message,"to server")
            UDPWorkerSocket.sendto(message,address)
        else:
            print("worker recived invalid message")
            encode(hasAddress,destAddress,message,cons.REJ)
            UDPWorkerSocket.sendto(message,address)
    except:
        continue

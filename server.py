# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from encode import encode
from encode import decode

def isWorker(address:tuple):
    return address[0] == worker1AddressPort[0] and address[1] == worker1AddressPort[1]

def hasDest(address:tuple[str,int]):
    if address[0]=="-1":
        return False
    return True

localIP     = "pserver" #socket.gethostbyname(socket.gethostname())
localPort   = 50000
bufferSize  = 1024

msgFromServer       = "Hello From Server"

worker1AddressPort   = ("pworker", 50000)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening @", UDPServerSocket.getsockname())


# Listen for incoming datagrams
while(True):        
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    destAddress,input, message = decode(message)
    if not hasDest(destAddress):
        destAddress = address

    if input:
        workerMsg = "Message from Worker:{}".format(message)
        workerIP  = "Worker IP Address:{}".format(address)
        print(workerMsg)
        print(workerIP)
        
        bytesToSend = encode(destAddress,message,input)
        print("server sending", bytesToSend, "to worker @", destAddress)
        UDPServerSocket.sendto(bytesToSend,worker1AddressPort)
    else:
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)

        print(clientMsg)
        print(clientIP)
        bytesToSend = encode(destAddress,message,input)
        print("server sending", bytesToSend, "to client")
        UDPServerSocket.sendto(bytesToSend,destAddress)


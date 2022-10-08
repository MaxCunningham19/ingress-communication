# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from encode import decode
from encode import encode
import constants as cons


server_address    = ("pserver",50000)
localIP     = socket.gethostbyname(socket.gethostname)
localPort   = 50000
bufferSize  = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPWorkerSocket.bind((localIP, localPort))

connecting = True
while connecting:
    UDPWorkerSocket.sendto(encode((localIP,localPort),b'0',cons.WORKER),server_address)
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    address, operation, message = decode(bytesAddressPair[0])
    if address is not None:
        if cons.isACK(operation):
            print("UDP worker up and listening @",  localIP, localPort)
            connecting = False

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPWorkerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    serverMsg = "Message from Server:{}".format(message)
    serverIP  = "Server IP Address:{}".format(address)
    print(serverMsg)
    print(serverIP)

    destAddress,input, message = decode(message)
    if destAddress is not None:
        clientIP = "Client Ip Address:{}".format(destAddress)
        print(clientIP)
        message = encode(destAddress, message,False)
        print("worker sending",message,"to server")
        UDPWorkerSocket.sendto(message,address)
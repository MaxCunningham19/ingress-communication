# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket
from encode import decode
from encode import encode


host = socket.getfqdn()
localIP     = "pworker" #socket.gethostbyname(host)
localPort   = 50000
bufferSize  = 1024

# Create a datagram socket
UDPWorkerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPWorkerSocket.bind((localIP, localPort))

print("UDP worker up and listening @",host,  localIP, localPort)

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

    clientIP = "Client Ip Address:{}".format(destAddress)
    print(clientIP)
    message = encode(destAddress, message,False)
    print("worker sending",message,"to server")
    UDPWorkerSocket.sendto(message,address)
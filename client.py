# based on https://pythontic.com/modules/socket/udp-client-server-example
import socket

from encode import encode
from encode import decode

msgFromClient       = "filename.txt"
serverAddressPort   = ("pserver", 50000)
bufferSize          = 1024

localIP     = (socket.gethostbyname(socket.gethostname()))
localPort   = 50000

print("UDP client up and listening @", localIP, localPort)


# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket
bytesToSend = encode(originalAddress=None,file=msgFromClient,input=True)
print("sending to server @",serverAddressPort)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
msg = "Message from Server {}".format(msgFromServer[0])
print(msg)

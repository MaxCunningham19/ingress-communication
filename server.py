# based on https://pythontic.com/modules/socket/udp-client-server-example
from typing import List
import socket
import constants as cons
from encode import encode
from encode import decode
import server_worker as swork
from server_util import recieve, add_worker, select_worker, get_worker, get_pair, pair_to_remove, add_pair

localIP = "server"
localPort = 50000
bufferSize = 1024


msgFromServer = "Hello From Server"
workers: List[swork.Worker] = []

connections = []

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening @", UDPServerSocket.getsockname())


# Listen for incoming datagrams
while (True):
    origAddress, input, message, num, address = recieve(UDPServerSocket,bufferSize)
    origAddress = (socket.gethostbyname(origAddress[0]), origAddress[1])
    if message is not None:
        if cons.isAddWorker(input):
            if add_worker(workers, address):
                workers.append(swork.Worker(address, False))
                workerMsg = "Adding Worker " + \
                    address[0] + " : " + str(address[1])
                print(workerMsg)
            message = encode(origAddress, message, cons.ACK, num)
            UDPServerSocket.sendto(message, address)

        elif cons.isGet(input):
            pair = get_pair(connections, address)
            if pair is None:
                index = select_worker(workers)
                if index == -1:
                    UDPServerSocket.sendto(
                        encode(origAddress, message, cons.BUSY, num), address)

                else:
                    print("establishing connection between",
                          workers[index].address, "and", address)
                    UDPServerSocket.sendto(
                        encode(origAddress, message, cons.GET, num), workers[index].address)
                    workers[index].busy = True
                    connections = add_pair(connections, address, workers[index].address)
            else:
                UDPServerSocket.sendto(
                        encode(origAddress, message, cons.REJ, num), address)

        elif cons.isDone(input):
            index = get_worker(workers, address)
            if index != -1: # is a worker
                pair_index = pair_to_remove(connections,address)
                if pair_index != -1:
                    print("closing connection between",
                          workers[index].address, "and", address)
                    del connections[pair_index]
                UDPServerSocket.sendto(encode(origAddress, message, cons.ACK, num), address)
            else:
                UDPServerSocket.sendto(encode(origAddress, message, cons.REJ, num), address)

        else:
            pair_adrs = get_pair(connections, address)
            if pair_adrs is None:
                UDPServerSocket.sendto(encode(origAddress, message, cons.REJ, num), address)
            else:
                UDPServerSocket.sendto(encode(origAddress, message, input, num), pair_adrs)
    else:
        print("cannot handle recieved message")

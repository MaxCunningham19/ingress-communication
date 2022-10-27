import socket
import server_worker as swork
from typing import List
from encode import decode

def recieve(UDPSocket: socket.socket, bufferSize:int):
    while True:
        try:
            bytesAddressPair = UDPSocket.recvfrom(bufferSize)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
            input, num, message = decode(message)
            return input, message, num, address
        except TimeoutError:
            continue


def add_worker(workers: List[swork.Worker], address) -> bool:
    for i in range(len(workers)):
        if workers[i].isAddress(address):
            return False
    return True


def select_worker(workers: List[swork.Worker]) -> int:
    for i in range(len(workers)):
        if not workers[i].isBusy():
            return i
    return -1


def get_worker(workers: List[swork.Worker], address) -> int:
    for i in range(len(workers)):
        if workers[i].isAddress(address):
            return i
    return -1

def equals(address1,address2 )->bool:
    return address1[0]==address2[0] and address1[1]==address2[1] 

def get_pair(pairs:List, address):
    for i in range(len(pairs)):
        if equals(pairs[i][0],address):
            return pairs[i][1]
        if equals(pairs[i][1], address):
            return pairs[i][0]
    return None

def add_pair(pairs, address , address2):
    pairs.append((address,address2))
    return pairs

def pair_to_remove(pairs,address):
    for i in range(len(pairs)):
        if equals(pairs[i][1],address):
            return i
    return -1
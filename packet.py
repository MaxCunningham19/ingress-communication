
from ast import List

def packetatise(max_size:int, file:str):
    if len(file) > max_size:
        return file

    fileAsBytes = file.encode("utf-8")
    file_packets = []

    tmp = b''
    for i in range(fileAsBytes):
        tmp = tmp.join(fileAsBytes[i])
        if (i+1)%max_size==0 and i!=0:
            file_packets.append(tmp)
            tmp = b''

    return file_packets

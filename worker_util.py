from typing import List

def split(max_len:int,msg:str):
    msg_arr:List[bytes] = []
    i = 0
    while i+max_len < len(msg):
        msg_arr.append(msg[i:i+max_len].encode())
        i = i+max_len
    msg_arr.append(msg[i:].encode())
    return msg_arr


def getFile(filename:str):
    file = open(filename,'r')
    fileContent = file.read()
    return fileContent
from typing import List

def split(max_len:int,msg:str|bytes):
    if type(msg) == str:
        content = split_str(max_len,msg)
    else:
        content = split_bytes(max_len,msg)
    return content

def split_bytes(max_len:int,msg:bytes):
    msg_arr:List[bytes] = []
    i = 0
    while i+max_len < len(msg):
        msg_arr.append(msg[i:i+max_len])
        i = i+max_len
    msg_arr.append(msg[i:])
    return msg_arr

def split_str(max_len:int,msg:str):
    msg_arr:List[bytes] = []
    i = 0
    while i+max_len < len(msg):
        msg_arr.append(msg[i:i+max_len].encode())
        i = i+max_len
    msg_arr.append(msg[i:].encode())
    return msg_arr

def getFile(filename:str):
    try:
        file = open(filename,'rb')
        fileContent = file.read()
        return fileContent
    except:
        return b''
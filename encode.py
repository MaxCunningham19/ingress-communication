import constants as cons
import ipaddress as ip

address_length = 8

def encode(file: bytes | str, op: str, number:int):
    bytesToSend = []

    bytesToSend.append(cons.OP_BYTE[op])

    numInBytes = encodeNumber(number)
    bytesToSend.append(numInBytes)

    if type(file) == str:
        file = bytes(file, 'utf-8')

    bytesToSend.append(file)
    sending = bytes.join(b'',bytesToSend)
    return sending


def encodeNumber(number:int):
    number = number % 16
    number_hex = hex(number)
    bytesNum = number_hex[2].encode('utf-8')
    return bytesNum


def decode(message: bytes):
    operation = decodeOperation(message[0:1])
    if operation == "":
        return  None, None, None


    number = decodeNumber(message[1:2])    
    return operation, number, message[2:],


def decodeNumber(numInBytes:bytes):
    if len(numInBytes)!=1:
        return -1
    num = int(numInBytes,base=16)
    return num


def decodeOperation(byt:bytes):
    if len(byt)!=1:
        return ""
    return cons.BYTE_OP[byt]

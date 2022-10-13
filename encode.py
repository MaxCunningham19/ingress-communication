import constants as cons
import ipaddress as ip

address_length = 8

def encode(addressIsSet:bool,originalAddress: tuple[str, int], file: bytes | str, op: str):
    bytesToSend = []

    if addressIsSet:
        bytesToSend.append(b'1')
    else:
        bytesToSend.append(b'0')

    byteAddress, bytePort = encodeAddress(originalAddress)
    bytesToSend.append(byteAddress)
    bytesToSend.append(bytePort)
    

    bytesToSend.append(cons.OP_BYTE[op])

    if type(file) == str:
        file = bytes(file, 'utf-8')

    bytesToSend.append(file)
    sending = bytes.join(b'',bytesToSend)
    return sending


def encodeAddress(address: tuple[str, int]):
    bytesAdrs = bytes(address[0],'utf-8').hex()
    bytesPort = address[1].to_bytes(2,'big').hex()
    return bytes(bytesAdrs,'utf-8'), bytes(bytesPort,'utf-8')


def decode(message: bytes):
    hasAdrs = False
    hasAdrs_byte = message[0:1]
    if hasAdrs_byte == b'1':
        hasAdrs = True

    address = cons.NOT_ADDRESS
    if hasAdrs:
        byte_address = message[1:9]
        byte_port= message[9:13]
        IPaddress = decodeAddress(byte_address)
        if IPaddress == "":
            return None, None, None, None
        port = decodePort(byte_port)
        if port == "":
            return None, None, None, None
        address = (IPaddress,port)
    
    operation = decodeOperation(message[13:14])
    if operation == "":
        return None, None, None, None
    return hasAdrs, address, operation,message[14:]



def decodeOperation(byt:bytes):
    if len(byt)!=1:
        return ""
    return cons.BYTE_OP[byt]


def decodePort(byte_port):
    if len(byte_port)!=4:
        return ""
    return int(byte_port, base=16)

def decodeAddress(byte_address:bytes):
    if len(byte_address) != address_length:
        return ""
    address = bytes.fromhex(str(int(byte_address,base=16))).decode('utf-8')
    return address 

def getDecimal(byt:bytes):
    if len(byt)!=2 :
        return "0"
    return str(int(byt, base=16))
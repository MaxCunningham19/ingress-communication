import constants as cons
import ipaddress as ip

address_length = 8

def encode(originalAddress: tuple[str, int], file: bytes | str, op: str, number:int):
    bytesToSend = []

    byteAddress, bytePort = encodeAddress(originalAddress)
    bytesToSend.append(byteAddress)
    bytesToSend.append(bytePort)
    

    bytesToSend.append(cons.OP_BYTE[op])

    numInBytes = encodeNumber(number)
    bytesToSend.append(numInBytes)

    if type(file) == str:
        file = bytes(file, 'utf-8')

    bytesToSend.append(file)
    sending = bytes.join(b'',bytesToSend)
    return sending


def encodeAddress(address: tuple[str, int]):
    bytesAdrs = ip.IPv4Address(address[0]).packed.hex()
    bytesPort = address[1].to_bytes(2,'big').hex()
    return bytes(bytesAdrs,'utf-8'), bytes(bytesPort,'utf-8')


def encodeNumber(number:int):
    number = number % 16
    print(number)
    number_hex = hex(number)
    print(number_hex)
    bytesNum = number_hex[2].encode('utf-8')
    print(bytesNum)
    return bytesNum


def decode(message: bytes):
    byte_address = message[0:8]
    byte_port= message[8:12]
    IPaddress = decodeAddress(byte_address)
    if IPaddress == "":
        return None, None, None
    port = decodePort(byte_port)
    if port == "":
        return None, None, None
    address = (IPaddress,port)
    
    operation = decodeOperation(message[12:13])
    if operation == "":
        return  None, None, None


    number = decodeNumber(message[13:14])    
    return address, operation,message[14:], number


def decodeNumber(numInBytes:bytes):
    if len(numInBytes)!=1:
        return -1
    num = int(numInBytes,base=16)
    return num


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
    i = 0
    address = ""
    while i<3:
        address = address + getDecimal(byte_address[i*2:i*2+2])+ "."
        i = i + 1
    address = address + getDecimal(byte_address[len(byte_address)-2:])
    return address 


def getDecimal(byt:bytes):
    if len(byt)!=2 :
        return "0"
    return str(int(byt, base=16))
def encode(addressIsSet:bool,originalAddress: tuple[str, int], file: bytes | str, op: str)->bytes:
    bytes_to_send = []

    if addressIsSet:
        bytes_to_send.append(b'1')
    else:
        bytes_to_send.append(b'0')
    bytes_to_send.append(bytes(originalAddress[0],'utf-8'))
    bytesPort = originalAddress[1].to_bytes(2,'big').hex()
    bytes_to_send.append(bytes(bytesPort,'utf-8'))
    if type(file) == str:
        file = bytes(file, 'utf-8')
    bytes_to_send.append(file)

    bytes_to_send.append(bytes(op,'utf-8'))
    sending = bytes.join(b'_',bytes_to_send)
    return sending


def decode(msg:bytes):
    bytes_rec = msg.split(b'_')
    hasAddress = bytes_rec[0]==b'1'
    ip = str.removesuffix(str.removeprefix(bytes_rec[1].decode('utf-8'),"'"),"'")
    adrs = (ip,int(bytes_rec[2],base=16))
    return hasAddress, adrs, bytes_rec[4].decode('utf-8'), bytes_rec[3].decode('utf-8')
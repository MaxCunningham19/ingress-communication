WORKER = "worker"
GET = "get"
RESP = "resp"
ACK = "ack"
OP = [WORKER, GET, RESP, ACK]

OP_BYTE = {str(WORKER):b'0',str(GET):b'1',str(RESP):b'2',str(ACK):b'3'}
BYTE_OP = {b'0':WORKER,b'1':GET,b'2':RESP,b'3':ACK}
WORKER = "worker"
GET = "get"
RESP = "resp"
ACK = "ack"
BUSY = "busy"
REJ = "rejected"
OP = [WORKER, GET, RESP, ACK,BUSY, REJ]

OP_BYTE = {str(WORKER):b'0',str(GET):b'1',str(RESP):b'2',str(ACK):b'3',BUSY:b'4',REJ:b'5'}
BYTE_OP = {b'0':WORKER,b'1':GET,b'2':RESP,b'3':ACK, b'4':BUSY,b'5':REJ}

def isACK(s:str)->bool:
    return s == ACK

def isAddWorker(s:str)->bool:
    return s == WORKER

def isResp(s:str)->bool:
    return s==RESP

def isGet(s:str)->bool:
    return s==GET
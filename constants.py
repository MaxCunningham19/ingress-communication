WORKER = "worker"
GET = "get"
RESP = "resp"
ACK = "ack"
BUSY = "busy"
REJ = "rejected"
DONE = "done"
OP = [WORKER, GET, RESP, ACK,BUSY, REJ, DONE]
OP_BYTE = {str(WORKER):b'0',str(GET):b'1',str(RESP):b'2',str(ACK):b'3',BUSY:b'4',REJ:b'5', DONE:b'6'}
BYTE_OP = {b'0':WORKER,b'1':GET,b'2':RESP,b'3':ACK, b'4':BUSY,b'5':REJ,b'6':DONE}
MAX_MSG_LENGTH = 1000

def isACK(s:str|None)->bool:
    if s is None:
        return False
    return s == ACK

def isAddWorker(s:str|None)->bool:
    if s is None:
        return False
    return s == WORKER

def isResp(s:str|None)->bool:
    if s is None:
        return False
    return s==RESP

def isGet(s:str|None)->bool:
    if s is None:
        return False
    return s==GET

def isBusy(s:str|None)->bool:
    if s is None:
        return False
    return s==BUSY

def isRej(s:str|None)->bool:
    if s is None:
        return False
    return s==REJ

def isDone(s:str|None)->bool:
    if s is None:
        return False
    return s==DONE

NOT_ADDRESS = ("0.0.0.0",0)
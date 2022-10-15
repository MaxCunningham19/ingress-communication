import constants as cons
import encode as enc

class Test:
    def __init__(self,name,input,output):
        self.name = name
        self.input = input
        self.output = output

class inp:
    def __init__(self,originalAddress: tuple[str, int], file: bytes | str, input: cons.OP, number:int):
        self.adrs = originalAddress
        self.file = file
        self.input = input
        self.number = number


def test_encodeAddress()->None:
    tests = [Test("one",("172.20.0.0",1),(b'ac140000',b'0001'))]

    hasFail = False
    for test in tests:
        result = enc.encodeAddress(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("encode address done")
    assert (hasFail==False)
    


def test_encode()->None:
    tests = [Test("add Worker",inp(("172.20.0.0",1),"file",cons.WORKER,17),b'ac140000000101file')]

    hasFail = False
    for test in tests:
        result = enc.encode(test.input.adrs,test.input.file,test.input.input,test.input.number)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("encode done")
    assert (hasFail==False)



def test_decodeDecimal()->None:
    tests = [Test("simple",b'ac',"172")]

    hasFail = False
    for test in tests:
        result = enc.getDecimal(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("decodeDecimal done")
    assert (hasFail==False)

def test_decodeAddress()->None:
    tests = [Test("one",b'ac140000',"172.20.0.0")]

    hasFail = False
    for test in tests:
        result = enc.decodeAddress(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("decode address done")
    assert (hasFail==False)

def test_decodePort()->None:
    tests = [
        Test("one",b'0001',1),
        Test("bigger",b'FFFF',65535),
    ]

    hasFail = False
    for test in tests:
        result = enc.decodePort(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("decode port done")
    assert (hasFail==False)
    
def test_decode()->None:
    tests = [Test("add Worker decoded",b'ac14000000010Afile',(("172.20.0.0",1),cons.WORKER,b'file',10))]

    hasFail = False
    for test in tests:
        result = enc.decode(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("decode done")
    assert (hasFail==False)
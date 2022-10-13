import constants as cons
import encode as enc

class Test:
    def __init__(self,name,input,output):
        self.name = name
        self.input = input
        self.output = output

class inp:
    def __init__(self,hasAdrs:bool,originalAddress: tuple[str, int], file: bytes | str, input: cons.OP):
        self.adrs = originalAddress
        self.hasAdrs = hasAdrs
        self.file = file
        self.input = input

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
    

def test_enctode():
    input = (True,("172.20.0.0",1),"file",cons.WORKER)
    assert (input==enc.decode(enc.encode(input[0],input[1],input[2],input[3])))


def test_encode()->None:
    tests = [Test("add Worker",inp(True,("172.20.0.0",1),"file",cons.WORKER),b'1ac14000000010file')]

    hasFail = False
    for test in tests:
        result = enc.encode(test.input.hasAdrs,test.input.adrs,test.input.file,test.input.input)
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
    tests = [Test("add Worker decoded",b'1ac14000000010file',(True,("172.20.0.0",1),cons.WORKER,b'file'))]

    hasFail = False
    for test in tests:
        result = enc.decode(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("decode done")
    assert (hasFail==False)
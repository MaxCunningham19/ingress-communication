import constants as cons
import encode as enc

class Test:
    def __init__(self,name,input,output):
        self.name = name
        self.input = input
        self.output = output

class inp:
    def __init__(self, file: bytes | str, input: cons.OP, number:int):
        self.file = file
        self.input = input
        self.number = number

def test_encode()->None:
    tests = [Test("add Worker",inp("file",cons.WORKER,17),b'01file')]
    hasFail = False
    for test in tests:
        result = enc.encode(test.input.file,test.input.input,test.input.number)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("encode done")
    assert (hasFail==False)

    
def test_decode()->None:
    tests = [Test("add Worker decoded",b'0Afile',(cons.WORKER,10,b'file'))]

    hasFail = False
    for test in tests:
        result = enc.decode(test.input)
        if result != test.output:
            print("Test",test.name,"failed expected:",test.output,"got:",result)
            hasFail = True
    print("decode done")
    assert (hasFail==False)
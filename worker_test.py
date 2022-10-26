import worker_util as wrkr

def test_split()->None:
    tests = [
        ("123456",7,[b'123456']),
        ("12341234",4,[b'1234',b'1234']),
        ("123456789",4, [b'1234',b'5678',b'9'])
    ]

    hasFail = False
    for test in tests:
        res = wrkr.split(test[1],test[0])
        if res != test[2]:
            hasFail = True
            print("split(",test[1],",",test[0],") expected:",test[2],"got:",res)
    assert hasFail == False

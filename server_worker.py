class Worker:
    def __init__(self,address:tuple(str,int),busy: bool):
        self.address = address
        self.busy = busy

    def isBusy(self)->bool:
        return self.busy

    def sent(self):
        self.busy = True

    def recieved(self):
        self.busy = False

    def isAddress(self,address:tuple(str,int))->bool:
        return self.address[0] == address[0] and self.address[1] == address[1]
from typing import Union
class Worker:
    def __init__(self, address,busy: bool):
        self.address = address
        self.busy = busy

    def isBusy(self)->bool:
        return self.busy

    def sent(self):
        self.busy = True

    def recieved(self):
        self.busy = False

    def isAddress(self,address)->bool:
        return self.address[0] == address[0] and self.address[1] == address[1]
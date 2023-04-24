import time

class Item():
    def __init__(self, price, username=None, timer=20) -> None:
        self.startTime = time.time()
        self.price = price
        self.priceChangeTime = self.startTime
        self.username = self.prevUsername = username
        self.timer = timer # biddable time (second)

    def isBiddable(self):
        curTime = time.time()
        return curTime - self.startTime <= self.timer

    def change_priceAndOwner(self, newPrice, newUsername):
        if newPrice > self.price and self.priceChangeTime != time.time() and self.isBiddable():
            self.price = newPrice
            self.prevUsername = self.username
            self.username = newUsername
            return True
        else:
            return False
import socket, threading, sys, os, struct, argparse, pickle, json
from typing import *

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import *
from pglib import *

class TCPThreadedClient():
    def __init__(self, args: argparse.Namespace) -> None:
        self.HOST = args.hostname
        self.PORT = args.port
        self.SOCK_ADDR = (self.HOST, self.PORT)

        try:
            self.mainSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print('[ERROR] Failed to create mSocket.', e)
            sys.exit()

        try:
            self.recvSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print('[ERROR] Failed to create recvSocket.', e)
            sys.exit()

        self.lastInput = ""

        

    def connect(self):
        try:
            self.mainSock.connect(self.SOCK_ADDR)
        except Exception as e:
            print("[ERROR] (mSocket) Something went wrong while connecting to server", e)
            sys.exit()

        try:
            self.recvSock.connect(self.SOCK_ADDR)
        except Exception as e:
            print("[ERROR] (recvSocket) Something went wrong while connecting to server", e)
            sys.exit()

        sendThread = threading.Thread(target=self.sendHandler)
        recvThread = threading.Thread(target=self.recvHandler)
        sendThread.start()
        recvThread.start()


    def sendHandler(self):
        mainSock = self.mainSock
        try:
            serverPubkey = recvDataStream(mainSock)

            sendDataStream(mainSock, args.username)
            usrExistAck = recvAck(mainSock)
            if usrExistAck != 1:
                while True:
                    password = input("Enter user's password: ").strip()
                    sendDataStream(mainSock, encrypt(password.encode(), serverPubkey))
                    pwAck = recvAck(mainSock)
                    if pwAck == 1: break
            else:
                password = input("Register user's password: ")
                sendDataStream(mainSock, encrypt(password.encode(), serverPubkey))
            print(recvDataStream(mainSock).decode())

            clientPubKey = getPubKey()
            sendDataStream(mainSock, clientPubKey)


            while True:
                op = self.lastInput = input("> ")
                sendDataStream(mainSock, op)

                if op == "EX":
                    mainSock.close()
                    self.recvSock.close()
                    break
                
                elif op == "BID":
                    biddable = json.loads(recvDataStream(mainSock).decode())
                    print("Biddable Items:\n", biddable)


                    itemname = input("What item you want to bid on: ")
                    sendDataStream(mainSock, itemname.encode())
                    itemnameAck = recvAck(mainSock)
                    if itemnameAck != 1: 
                        print("Item was not found")
                        continue
                    newPrice = input("How much money: ")
                    sendDataStream(mainSock, str(newPrice))

                    newPriceAck = recvAck(mainSock)
                    print("Successful" if newPriceAck==1 else "Unsuccessful. Time collision or price too low")

                elif op == "GETALL":
                    data = json.loads(recvDataStream(mainSock).decode())
                    print(data)

                elif op == "AUCT": # sell something
                    while True:
                        itemname = input("Give a unique item name: ")
                        sendDataStream(mainSock, itemname)
                        if recvAck(mainSock) == 1 : break

                    while True:
                        price = input("Give a starting price: ")
                        try:
                            _ = int(price)
                            break
                        except:
                            print("Enter number (integer)")
                            continue
                    sendDataStream(mainSock, price)
                    print("Successful" if recvAck(mainSock) == 1 else "Unsuccessful")


        except Exception as e:
            print(e)
            sendDataStream(mainSock, "EX")
            mainSock.close()
            self.recvSock.close()
        except KeyboardInterrupt as e:
            print("[INFO] Shutting down connection manually...")
            sendDataStream(mainSock, "EX")
            mainSock.close()
            self.recvSock.close()

        


    def recvHandler(self):
        recvSock = self.recvSock
        try:
            while True:
                encrpyted_msg = recvDataStream(recvSock)
                msg = decrypt(encrpyted_msg).decode()
                
                print("\n", msg)
                print("\r> ", end="")
        except Exception as e:
            if self.lastInput != "EX":
                print(f"[ERROR] Error occured in recvHandler: ", e)
            recvSock.close()




if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description="Chat Room Server")
    parser.add_argument("-hn", "--hostname", type=str, metavar="", default="127.0.0.1",
                        help="Hostname")
    parser.add_argument("-p", "--port", type=int, metavar="", default=9999,
                        help="port")
    parser.add_argument("-un", "--username", type=str, metavar="", default="jack",
                        help="enter a unique username")
    args = parser.parse_args()

    client = TCPThreadedClient(args)
    client.connect()
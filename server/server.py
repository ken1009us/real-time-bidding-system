import socket, threading, sys, os, struct, argparse, pickle, datetime, json
from typing import *

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from utils import *
from pglib import *

from item import *

USR_DBFN = "users.txt"

class TCPThreadedServer():
    def __init__(self, args: argparse.Namespace) -> None:
        self.HOST = args.hostname
        self.PORT = args.port
        self.SOCK_ADDR = (self.HOST, self.PORT)

        self.items: Dict[str, Item] = {"car": Item(100), "pen": Item(200)}

        try:
            self.mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print('[ERROR] Failed to create socket.', e)
            sys.exit()
    
        try:
            self.mSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except Exception as e:
            print('[ERROR] Failed to set socket option.', e)
            sys.exit()

        try:
            self.mSocket.bind(self.SOCK_ADDR)
        except socket.error as e:
            print('[ERROR] Failed to bind socket.', e)
            sys.exit()

        self.activeUsers: Dict[str, socket.socket] = {}
        self.userPubkeys: Dict[str, bytes] = {}
        self.userDB: Dict[str, str] = {}

        
        if not os.path.isfile(USR_DBFN):
            file = open(USR_DBFN, "w+")
            file.close()
        with open(USR_DBFN, "r") as f:
            for line in f:
                username, password = [x.strip() for x in line.split(" ")]
                self.userDB[username] = password




    def listen(self):
        self.mSocket.listen()
        print(f"[INFO] Listening on {self.HOST}:{self.PORT}")

        try:
            while True:
                client, addr = self.mSocket.accept()
                clientRecv, clientRecv_addr = self.mSocket.accept()
                # client.settimeout(60)

                t = threading.Thread(target=self.clientHandler, args=(client, clientRecv, addr))
                t.start()

        except KeyboardInterrupt:
            print(f"\r[INFO] Server shut down manually")
            



    
    def clientHandler(self, clientMain: socket.socket, clientRecv: socket.socket, addr):
        serverPubkey = getPubKey()
        try:
            sendDataStream(clientMain, serverPubkey)
            username = recvDataStream(clientMain).decode().strip()
            
            sendAck(clientMain, 1 if not username in self.activeUsers.keys() else 0)


            if username in self.userDB.keys():
                sendAck(clientMain, 0)
                while True:
                    encrypted_pw = recvDataStream(clientMain)
                    received_pw = decrypt(encrypted_pw).decode().strip()
                    if received_pw != self.userDB[username]:
                        sendAck(clientMain, 0)
                    else:
                        sendAck(clientMain, 1)
                        break
            else:
                sendAck(clientMain, 1)
                encrypted_pw = recvDataStream(clientMain)
                received_pw = decrypt(encrypted_pw).decode().strip()
                self.userDB[username] = received_pw
                with open(USR_DBFN, "a") as f:
                    f.write(f"{username} {received_pw}\n")
            sendDataStream(clientMain, f"Hello, {username}")

            self.activeUsers[username] = clientRecv
            self.userPubkeys[username] = recvDataStream(clientMain)


            while True:
                op = recvDataStream(clientMain).decode()
                
                if op == "EX":
                    clientMain.close()
                    clientRecv.close()
                    self.activeUsers.pop(username)
                    break

                elif op == "BID":
                    sendDataStream(clientMain, json.dumps(self.getBiddableItems()))

                    itemname = recvDataStream(clientMain).decode()
                    if itemname in self.items:
                        sendAck(clientMain, 1)
                    else:
                        sendAck(clientMain, 0)
                        continue
                    newPrice = int(recvDataStream(clientMain).decode())

                    result = self.items[itemname].change_priceAndOwner(newPrice, username)
                    sendAck(clientMain, 1 if result else 0)
                    
                
                elif op == "GETALL":
                    items = self.transformItems()
                    sendDataStream(clientMain, json.dumps(items))

                elif op == "AUCT":
                    while True:
                        itemname = recvDataStream(clientMain).decode()
                        if itemname not in self.items.keys():
                            sendAck(clientMain, 1)
                            break
                        sendAck(clientMain, 0)

                    try:
                        itemprice = int(recvDataStream(clientMain).decode())
                        self.items[itemname] = Item(itemprice, username)
                        sendAck(clientMain, 1)
                    except Exception as e:
                        print(e)
                        sendAck(clientMain, 0)
                        continue


                    for k, v in self.activeUsers.items():
                        sendDataStream(v, encrypt(f"New item in auction: {itemname}".encode(), 
                                                self.userPubkeys[k]))
                    

        except Exception as e: 
            print(f"[ERROR] error occurs for user: {username}\n", e)




    def transformItems(self):
        tmp = {}
        for k in self.items.keys():
            tmp[k] = {}
            v = self.items[k]
            tmp[k]["price"] = v.price
            tmp[k]["owner"] = v.username
            tmp[k]["isBiddable"] = v.isBiddable()
        return tmp

    
    def getBiddableItems(self):
        tmp = {}
        for k in self.items.keys():
            v = self.items[k]
            if v.isBiddable():
                tmp[k] = {}
                tmp[k]["price"] = v.price
                tmp[k]["username"] = v.username
        return tmp


    






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Bidding System Server")
    parser.add_argument("-hn", "--hostname", type=str, metavar="", default="127.0.0.1",
                        help="Hostname")
    parser.add_argument("-p", "--port", type=int, metavar="", default=9999,
                        help="port")
    args = parser.parse_args()

    server = TCPThreadedServer(args)
    server.listen()

        
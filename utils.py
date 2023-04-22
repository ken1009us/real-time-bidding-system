import json


import socket, datetime, sys, os
from typing import *


BUFFER = 1024




def addrToString(addr: Tuple[str, str]):
    return f"{addr[0]}:{addr[1]}"


def sendAck(conn: socket.socket, ack: int):
    data = str(ack)
    payload = f"{data:<64}"
    conn.sendall(payload.encode("utf-8"))


def recvAck(conn: socket.socket) -> Union[int, None]:
    data = conn.recv(64).decode().strip()
    return int(data)


def sendDataStream(conn: socket.socket, data: Union[str, bytes]):
    data_encoded = data.encode() if type(data) == str else data
    size = len(data_encoded)
    size_segment = f"{size:<{BUFFER}}".encode()

    conn.sendall(size_segment)

    res = recvAck(conn)

    if res != 1:
        print("[ERROR] receiver did not recive correct size segment")
        return

    i = 0
    while i * BUFFER < size:
        payload = data_encoded[i*BUFFER : (i+1)*BUFFER]
        conn.sendall(payload)
        i += 1


def recvDataStream(conn: socket.socket) -> bytes:
    size_segment = conn.recv(BUFFER).decode()

    try:
        size = int(size_segment.strip())
        if size < 0: raise Exception("Size is smaller than 0")
        sendAck(conn, 1)
    except Exception as e:
        print(e)
        sendAck(conn, -1)

    data = b""
    while len(data) < size:
        data += conn.recv(BUFFER)

    return data

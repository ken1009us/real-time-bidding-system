import socket

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

# create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_socket.bind((TCP_IP, TCP_PORT))
tcp_socket.listen(1)

# wait for a client connection
print('Waiting for a client connection...')
client_socket, client_address = tcp_socket.accept()
print(f'Client connected from {client_address}')

# handle client requests
while True:
    # receive data from client
    data = client_socket.recv(BUFFER_SIZE)
    if not data:
        break
    # process client request
    # TODO: Implement bidding process using TCP


    # send response back to client
    client_socket.send(data)

# close the connection
client_socket.close()
tcp_socket.close()

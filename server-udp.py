import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5006
BUFFER_SIZE = 1024

# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((UDP_IP, UDP_PORT))

# wait for client messages
while True:
    data, client_address = udp_socket.recvfrom(BUFFER_SIZE)
    # process client message
    # TODO: Implement real-time updates using UDP


    # send response back to client
    udp_socket.sendto(data, client_address)

# close the connection
udp_socket.close()

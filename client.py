import socket

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 1024

UDP_IP = "127.0.0.1"
UDP_PORT = 5006

# create a TCP socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_IP, TCP_PORT))

# create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# authenticate user
username = input('Username: ')
password = input('Password: ')
login_credentials = f'{username},{password}'
tcp_socket.send(login_credentials.encode())
response = tcp_socket.recv(BUFFER_SIZE).decode()
if response == 'Authentication successful':
    print('Login successful')
else:
    print('Login failed')
    tcp_socket.close()
    exit()

# handle user input
while True:
    command = input('Enter command (bid, quit): ')
    if command == 'bid':
        # TODO: Implement bidding process
        pass
    elif command == 'quit':
        break
    else:
        print('Invalid command')

# close the connection
tcp_socket.close()
udp_socket.close()

import socket
from app.globals import DEFAULT_PORT, MAX_BUF, LOOPBACK_ADDRESS

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (LOOPBACK_ADDRESS, DEFAULT_PORT)

message = input('Send a message to the server').encode()  # message to test the socket

client.sendto(message, address)
try:
    data, server = client.recvfrom(MAX_BUF)
    print(data.decode())
except socket.timeout:
    print('request timed out...')

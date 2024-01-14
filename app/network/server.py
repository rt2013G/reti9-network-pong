from app.globals import DEFAULT_PORT, MAX_BUF
import socket

# Create the socket and bind to the port
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('', DEFAULT_PORT))

while True:
    message, address = server.recvfrom(MAX_BUF)
    server.sendto(message, address)

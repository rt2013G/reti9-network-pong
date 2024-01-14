import pickle
import socket
from app.globals import DEFAULT_PORT, MAX_BUF


class Server:
    # Initialize the class by creating the socket and binding to the port
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(('', DEFAULT_PORT))

    def receive_ball_data(self):
        data, address = self.server_socket.recvfrom(MAX_BUF)
        # uses pickle to convert bytes to a ball object
        ball_data = pickle.loads(data)
        print(str(ball_data))

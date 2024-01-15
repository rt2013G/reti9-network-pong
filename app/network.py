import pickle
import socket
from app.globals import DEFAULT_PORT, MAX_BUF
from app.components import Ball


class Peer:
    # Initialize the class by creating the socket and binding to the port
    # There should always only be one other peer, so it can just set it as a variable
    def __init__(self, paddle_id):
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_socket.bind(('', DEFAULT_PORT + paddle_id))
        self.other_peer = ('', DEFAULT_PORT + paddle_id)

    def set_other_peer(self, address, paddle_id):
        self.other_peer = (address, DEFAULT_PORT + paddle_id)

    def receive_ball_data(self):
        data, address = self.peer_socket.recvfrom(MAX_BUF)
        # uses pickle to convert bytes to a ball object
        ball_data = pickle.loads(data)
        print(str(ball_data))

    def send_ball_data(self):
        test_ball = Ball()
        data = pickle.dumps(test_ball)
        self.peer_socket.sendto(data, self.other_peer)

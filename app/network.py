import pickle
import socket
from app.globals import DEFAULT_PORT, MAX_BUF
from app.components import Paddle, Ball


class Peer:
    # Initialize the class by creating the socket and binding to the port
    # There should always only be one other peer, so it can just set it as a variable
    def __init__(self, paddle_id):
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_socket.bind(('', DEFAULT_PORT + paddle_id))
        self.id = paddle_id
        self.other_peer = ('', DEFAULT_PORT + paddle_id)
        self.is_seeder = False
        self.controlled_paddle = Paddle()
        self.other_peer_paddle = Paddle()
        self.ball = Ball()

    def set_other_peer(self, address, paddle_id):
        self.other_peer = (address, DEFAULT_PORT + paddle_id)

    def receive_data(self):
        self.peer_socket.settimeout(0.001)
        data, address = self.peer_socket.recvfrom(MAX_BUF)
        object_data = pickle.loads(data)
        return object_data

    def send_data(self, object_data):
        data = pickle.dumps(object_data)
        self.peer_socket.sendto(data, self.other_peer)

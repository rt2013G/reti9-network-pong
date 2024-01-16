import pickle
import socket
import time
from app.globals import DEFAULT_PORT, MAX_BUF, TIMEOUT, LEFT_PADDLE_ID, RIGHT_PADDLE_ID
from app.components import Paddle, Ball, Scorekeeper


class Peer:
    # Initializes the class by creating the socket and binding to the port
    # then creates the required game components
    # There should always only be one other peer, so it can just be set as a variable
    def __init__(self, paddle_id):
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_socket.bind(('', DEFAULT_PORT + paddle_id))
        self.id = paddle_id
        self.other_peer = ('', DEFAULT_PORT + paddle_id)
        self.controlled_paddle = Paddle()
        self.other_peer_paddle = Paddle()
        self.ball = Ball()
        self.scorekeeper = Scorekeeper()

    # Sets the other peer based on this peer's ID
    def set_other_peer(self, address):
        if self.id == LEFT_PADDLE_ID:
            self.other_peer = (address, DEFAULT_PORT + RIGHT_PADDLE_ID)
        else:
            self.other_peer = (address, DEFAULT_PORT + LEFT_PADDLE_ID)

    # Receives data from the socket and parses it using pickle
    def receive_data(self):
        self.peer_socket.settimeout(TIMEOUT)
        data, address = self.peer_socket.recvfrom(MAX_BUF)
        object_data = pickle.loads(data)
        return object_data

    # Obtains an object data using the function receive_data, then performs the appropriate action
    # based on the object's type
    def receive_and_replace_object_data(self):
        object_data = object
        try:
            object_data = self.receive_data()

        # If there's a timeout, meaning some packet loss, it just ignores it
        # the game will keep going albeit less responsive
        except socket.timeout:
            return

        # Fixes an error on starting the process:
        # if the other peer isn't available yet, this prevents the process to terminate
        except socket.error:
            print('waiting for the other peer...')
            time.sleep(1)

        if type(object_data) is Ball:
            self.ball = object_data
        elif type(object_data) is Paddle:
            self.other_peer_paddle = object_data
        elif type(object_data) is Scorekeeper:
            self.scorekeeper = object_data

    # Sends data to the other peer
    def send_data(self, object_data):
        data = pickle.dumps(object_data)
        self.peer_socket.sendto(data, self.other_peer)

import socket, pickle
from app.components import Ball
from app.globals import DEFAULT_PORT


class Client:
    def __init__(self, address):
        self.test_ball = Ball()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (address, DEFAULT_PORT)

    def send_ball_data(self):
        test_ball = Ball()
        data = pickle.dumps(test_ball)
        self.client_socket.sendto(data, self.address)

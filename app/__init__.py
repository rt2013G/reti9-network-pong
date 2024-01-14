import sys
import app.game as game


def start():
    # If there are no command line arguments, the process is the server
    # if there is a command line argument, it sets such argument as the address
    if len(sys.argv) == 1:
        # server
        from app.network.server import Server
        server = Server()
        server.receive_ball_data()
    elif len(sys.argv) == 2:
        from app.network.client import Client
        client = Client(str(sys.argv[1]))
        client.send_ball_data()
    else:
        print('error. usage: python.exe pong.py <address>')
        sys.exit(1)

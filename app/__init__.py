import sys
import app.game as game
from app.network import Peer
from app.utils import Args


def print_usage_message():
    print('error. usage: python.exe pong.py <paddle id, either 0 (left paddle) or 1 (right paddle)> '
          '<other peer address> <other peer paddle id>')


def start():
    # If there are no command line arguments, the process is the server
    # if there is a command line argument, it sets such argument as the address
    if len(sys.argv) == 4:
        try:
            peer_id = int(sys.argv[1])
            other_peer_address = str(sys.argv[2])
            other_peer_id = int(sys.argv[3])
            args = Args(peer_id=peer_id, other_peer_address=other_peer_address, other_peer_id=other_peer_id)
        except ValueError:
            print_usage_message()
            sys.exit(0)
        game.peer_run(args)
    else:
        print_usage_message()
        sys.exit(0)

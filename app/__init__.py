import sys
import app.game as game
from app.network import Peer
from app.utils import Args
from app.globals import LOOPBACK_ADDRESS


def print_usage_message():
    print('error. usage: python.exe pong.py <paddle id, either 0 (left paddle) or 1 (right paddle)> '
          '<other peer address>')


def start():
    # parses the command line arguments and passes them into the function that initializes the peer
    # and starts the game
    # peer_id: the id of local paddle (0 is the left paddle, 1 is the right paddle)
    # - the right paddle should be started first
    # other_peer_address: the IP address of the other paddle
    # if the other_peer_address is omitted, the loopback address is used
    if len(sys.argv) == 3:
        try:
            peer_id = int(sys.argv[1])
            other_peer_address = str(sys.argv[2])
            args = Args(peer_id=peer_id, other_peer_address=other_peer_address)
        except ValueError:
            print_usage_message()
            sys.exit(0)
        game.peer_run(args)
    elif len(sys.argv) == 2:
        try:
            peer_id = int(sys.argv[1])
            args = Args(peer_id=peer_id, other_peer_address=LOOPBACK_ADDRESS)
        except ValueError:
            print_usage_message()
            sys.exit(0)
        game.peer_run(args)
    else:
        print_usage_message()
        sys.exit(0)

import sys
import app.game as game
from app.network import Peer
from app.globals import LOOPBACK_ADDRESS
from app.utils import Args


def start():
    # If there are no command line arguments, the process is the server
    # if there is a command line argument, it sets such argument as the address
    if len(sys.argv) == 4:
        peer_id = int(sys.argv[1])
        other_peer_address = str(sys.argv[2])
        other_peer_id = int(sys.argv[3])
        args = Args(peer_id=peer_id, other_peer_address=other_peer_address, other_peer_id=other_peer_id)
        game.peer_run(args)
    else:
        print('error. usage: python.exe pong.py <paddle id> <other peer address> <other peer paddle id>')
        sys.exit(1)

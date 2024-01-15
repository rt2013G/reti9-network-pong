import sys
import app.game as game
from app.network import Peer
from app.globals import LOOPBACK_ADDRESS


def start():
    # If there are no command line arguments, the process is the server
    # if there is a command line argument, it sets such argument as the address
    if len(sys.argv) == 4:
        self_id = int(sys.argv[1])
        other_peer_address = str(sys.argv[2])
        other_peer_id = int(sys.argv[3])
        peer = Peer(self_id)
        peer.set_other_peer(other_peer_address, other_peer_id)
    else:
        print('error. usage: python.exe pong.py <peer address>')
        sys.exit(1)

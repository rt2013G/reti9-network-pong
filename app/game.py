import sys
import pygame
from app.globals import *
from app.network import Peer


# The Grid class represents the matrix that stores the position of all the objects.
# The objects are represented by symbolic characters, the display method converts each character
# into the appropriate color on the screen
class Grid:
    def __init__(self):
        self.matrix = [[EMPTY_CHAR for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    def update_grid(self, ball, left_paddle, right_paddle):
        self.matrix = [[EMPTY_CHAR for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

        for i in range(PADDLE_WIDTH):
            for j in range(GRID_HEIGHT):
                if left_paddle.pos_y - PADDLE_HEIGHT < j < left_paddle.pos_y + PADDLE_HEIGHT:
                    self.matrix[i][j] = PADDLE_CHAR

        for i in range(PADDLE_WIDTH):
            for j in range(GRID_HEIGHT):
                if right_paddle.pos_y - PADDLE_HEIGHT < j < right_paddle.pos_y + PADDLE_HEIGHT:
                    self.matrix[GRID_WIDTH - i - 1][j] = PADDLE_CHAR

        self.matrix[ball.pos_x][ball.pos_y] = BALL_CHAR

    def print_grid(self):
        for j in range(GRID_HEIGHT):
            for i in range(GRID_WIDTH):
                print(self.matrix[i][j], end='')
            print(EMPTY_CHAR)

    def display(self, screen):
        for j in range(GRID_HEIGHT):
            for i in range(GRID_WIDTH):
                if self.matrix[i][j] == PADDLE_CHAR:
                    pygame.draw.rect(screen, PADDLE_COLOR,
                                     (i * SCREEN_RATIO, j * SCREEN_RATIO, SCREEN_RATIO, SCREEN_RATIO))
                elif self.matrix[i][j] == BALL_CHAR:
                    pygame.draw.circle(screen, BALL_COLOR, (i * SCREEN_RATIO, j * SCREEN_RATIO),
                                       SCREEN_RATIO)


def peer_run(args):
    # Instantiates game variables
    grid = Grid()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Create a peer on the current process and set the other peer
    peer = Peer(args.peer_id)
    peer.set_other_peer(args.other_peer_address, args.other_peer_id)

    # The peer with id 0 controls the left paddle
    # the peer with id 1 controls the right paddle
    if peer.id == LEFT_PADDLE_ID:
        pygame.display.set_caption("Left paddle")
    else:
        pygame.display.set_caption("Right paddle")

    while True:
        screen.fill(SCREEN_COLOR)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_w:
                    peer.controlled_paddle.velocity = -1
                if i.key == pygame.K_s:
                    peer.controlled_paddle.velocity = 1

        # after the paddle moves, it sends the paddle data
        # then tries to get it from the other peer
        peer.controlled_paddle.move()
        peer.send_data(peer.controlled_paddle)

        peer.receive_and_replace_object_data()

        # next the peers handles the ball movement and sends the ball data
        if peer.ball.seeder_id == peer.id:
            if peer.id == 0:
                peer.ball.move(peer.controlled_paddle, peer.other_peer_paddle)
            else:
                peer.ball.move(peer.other_peer_paddle, peer.controlled_paddle)
            peer.send_data(peer.ball)
            if peer.ball.is_out():
                if peer.ball.pos_x <= 0:
                    peer.scorekeeper.add_score(left_paddle_scored=False)
                elif peer.ball.pos_x >= GRID_WIDTH:
                    peer.scorekeeper.add_score(left_paddle_scored=True)
                peer.ball.reset_position()
                peer.ball.set_random_velocity()
                peer.send_data(peer.ball)
                peer.send_data(peer.scorekeeper)
        else:
            peer.receive_and_replace_object_data()
            peer.receive_and_replace_object_data()

        try:
            if peer.id == 0:
                grid.update_grid(peer.ball, peer.controlled_paddle, peer.other_peer_paddle)
            else:
                grid.update_grid(peer.ball, peer.other_peer_paddle, peer.controlled_paddle)
        except IndexError:
            pass
        grid.display(screen)
        peer.scorekeeper.display(screen)
        pygame.display.flip()
        clock.tick(FPS)

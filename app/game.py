import pygame
import socket
from app.globals import *
from app.components import Ball, Paddle
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


# The Scorekeeper class holds the values of the players' scores
# the display methods
class Scorekeeper:
    def __init__(self):
        self.score_player_1 = 0
        self.score_player_2 = 0

    def update_score(self, ball):
        if ball.pos_x <= 0:
            self.score_player_2 += 1
        elif ball.pos_x >= GRID_WIDTH:
            self.score_player_1 += 1

    def display(self, screen):
        font = pygame.font.SysFont(SCORE_FONT, FONT_SIZE)
        player_a = font.render(str(self.score_player_1), False, TEXT_COLOR)
        screen.blit(player_a, (TEXT_WIDTH_SPACE, TEXT_HEIGHT_SPACE))
        player_b = font.render(str(self.score_player_2), False, TEXT_COLOR)
        screen.blit(player_b, (SCREEN_WIDTH - TEXT_WIDTH_SPACE, TEXT_HEIGHT_SPACE))


def peer_run(args):
    # Create a peer on the current process and set the other peer
    peer = Peer(args.peer_id)
    peer.set_other_peer(args.other_peer_address, args.other_peer_id)

    # The peer with id 0 controls the left paddle
    # the peer with id 1 controls the right paddle
    if peer.id == 0:
        # The left paddle starts as the initial seeder
        peer.is_seeder = True

    # Instantiates game variables
    grid = Grid()
    object_data = object
    scorekeeper = Scorekeeper()
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(SCREEN_COLOR)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_w:
                    peer.controlled_paddle.velocity = -1
                    peer.send_data(peer.controlled_paddle)
                if i.key == pygame.K_s:
                    peer.controlled_paddle.velocity = 1
                    peer.send_data(peer.controlled_paddle)

        try:
            object_data = peer.receive_data()
        except socket.timeout:
            pass

        if type(object_data) is Paddle:
            peer.other_peer_paddle = object_data
            peer.other_peer_paddle.move()

        peer.controlled_paddle.move()

        if peer.is_seeder:
            if peer.id == 0:
                peer.ball.move(peer.controlled_paddle, peer.other_peer_paddle)
            else:
                peer.ball.move(peer.other_peer_paddle, peer.controlled_paddle)
            peer.send_data(peer.ball)
            if peer.ball.is_out():
                scorekeeper.update_score(peer.ball)
                peer.ball.reset_position()
                peer.ball.set_random_velocity()
                peer.send_data(peer.ball)

        try:
            object_data = peer.receive_data()
        except socket.timeout:
            pass
        if type(object_data) is Ball:
            peer.ball = object_data
        elif type(object_data) is Paddle:
            peer.other_peer_paddle = object_data

        try:
            if peer.id == 0:
                grid.update_grid(peer.ball, peer.controlled_paddle, peer.other_peer_paddle)
            else:
                grid.update_grid(peer.ball, peer.other_peer_paddle, peer.controlled_paddle)
        except IndexError:
            pass
        grid.display(screen)
        scorekeeper.display(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

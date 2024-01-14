import pygame
from app.globals import *
from app.components import Ball, Paddle


# The Grid class represents the matrix that stores the position of all the objects.
# The objects are represented by symbolic characters, the display method converts each character
# into the appropriate color on the screen
class Grid:
    def __init__(self):
        self.matrix = [[EMPTY_CHAR for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    def update_grid(self, ball, paddle):
        self.matrix = [[EMPTY_CHAR for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

        for i in range(PADDLE_WIDTH):
            for j in range(GRID_HEIGHT):
                if paddle.pos_y - PADDLE_HEIGHT < j < paddle.pos_y + PADDLE_HEIGHT:
                    self.matrix[i][j] = PADDLE_CHAR

        for i in range(PADDLE_WIDTH):
            for j in range(GRID_HEIGHT):
                if paddle.pos_y - PADDLE_HEIGHT < j < paddle.pos_y + PADDLE_HEIGHT:
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


def run():
    grid = Grid()
    ball = Ball()
    paddle = Paddle()
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
                    paddle.velocity = -1
                if i.key == pygame.K_s:
                    paddle.velocity = 1

        paddle.move()
        ball.move(paddle)
        if ball.is_out():
            scorekeeper.update_score(ball)
            ball.reset_position()
            ball.set_random_velocity()
        grid.update_grid(ball, paddle)
        grid.display(screen)
        scorekeeper.display(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

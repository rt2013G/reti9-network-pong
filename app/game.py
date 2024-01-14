from app.components import Ball, Paddle
import pygame
from app.globals import *

grid = [[EMPTY_CHAR for j in range(GRID_HEIGHT)] for i in range(GRID_WIDTH)]

score_player_1 = 0
score_player_2 = 0

ball = Ball()
paddle = Paddle()


def make_grid():
    global paddle
    global ball
    temp_grid = [[EMPTY_CHAR for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    for i in range(PADDLE_WIDTH):
        for j in range(GRID_HEIGHT):
            if paddle.pos_y - PADDLE_HEIGHT < j < paddle.pos_y + PADDLE_HEIGHT:
                temp_grid[i][j] = PADDLE_CHAR

    for i in range(PADDLE_WIDTH):
        for j in range(GRID_HEIGHT):
            if paddle.pos_y - PADDLE_HEIGHT < j < paddle.pos_y + PADDLE_HEIGHT:
                temp_grid[GRID_WIDTH - i - 1][j] = PADDLE_CHAR

    temp_grid[ball.pos_x][ball.pos_y] = BALL_CHAR

    return temp_grid


def update_score():
    global score_player_1
    global score_player_2
    global ball
    if ball.pos_x <= 0:
        score_player_2 += 1
    elif ball.pos_x >= GRID_WIDTH:
        score_player_1 += 1


def run():
    global ball
    global paddle
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    global grid

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
            update_score()
            ball.reset_position()
            ball.set_random_velocity()
        grid = make_grid()
        draw_board(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def print_grid():
    for j in range(GRID_HEIGHT):
        for i in range(GRID_WIDTH):
            print(grid[i][j], end='')
        print(EMPTY_CHAR)


def draw_board(screen):
    global ball
    font = pygame.font.SysFont(SCORE_FONT, FONT_SIZE)
    player_a = font.render(str(score_player_1), False, TEXT_COLOR)
    screen.blit(player_a, (TEXT_WIDTH_SPACE, TEXT_HEIGHT_SPACE))
    player_b = font.render(str(score_player_2), False, TEXT_COLOR)
    screen.blit(player_b, (SCREEN_WIDTH - TEXT_WIDTH_SPACE, TEXT_HEIGHT_SPACE))

    for j in range(GRID_HEIGHT):
        for i in range(GRID_WIDTH):
            if grid[i][j] == PADDLE_CHAR:
                pygame.draw.rect(screen, PADDLE_COLOR, (i * SCREEN_RATIO, j * SCREEN_RATIO, SCREEN_RATIO, SCREEN_RATIO))
            elif grid[i][j] == BALL_CHAR:
                pygame.draw.circle(screen, BALL_COLOR, (ball.pos_x * SCREEN_RATIO, ball.pos_y * SCREEN_RATIO),
                                   SCREEN_RATIO)

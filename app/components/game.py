import random
import pygame
from app.globals import *

grid = [[EMPTY_CHAR for j in range(GRID_HEIGHT)] for i in range(GRID_WIDTH)]

paddle_pos_y = GRID_HEIGHT / 2

ball_pos_x = int(GRID_WIDTH / 2)
ball_pos_y = int(GRID_HEIGHT / 2)

paddle_velocity = 0

score_player_1 = 0
score_player_2 = 0

ball_velocity_x = 0
ball_velocity_y = 0


def set_random_velocity():
    global ball_velocity_x
    global ball_velocity_y

    # velocity on both axis should be either +1 or -1
    if random.choice([True, False]):
        ball_velocity_x = 1
    else:
        ball_velocity_x = -1

    if random.choice([True, False]):
        ball_velocity_y = 1
    else:
        ball_velocity_y = -1


def make_grid():
    temp_grid = [[EMPTY_CHAR for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    for i in range(PADDLE_WIDTH):
        for j in range(GRID_HEIGHT):
            if paddle_pos_y - PADDLE_HEIGHT < j < paddle_pos_y + PADDLE_HEIGHT:
                temp_grid[i][j] = PADDLE_CHAR

    for i in range(PADDLE_WIDTH):
        for j in range(GRID_HEIGHT):
            if paddle_pos_y - PADDLE_HEIGHT < j < paddle_pos_y + PADDLE_HEIGHT:
                temp_grid[GRID_WIDTH - i - 1][j] = PADDLE_CHAR

    temp_grid[ball_pos_x][ball_pos_y] = BALL_CHAR

    return temp_grid


def move_paddle(velocity):
    global paddle_pos_y
    paddle_pos_y += velocity
    if paddle_pos_y <= PADDLE_HEIGHT - 1:
        paddle_pos_y = PADDLE_HEIGHT - 1
    elif paddle_pos_y >= GRID_HEIGHT - PADDLE_HEIGHT:
        paddle_pos_y = GRID_HEIGHT - PADDLE_HEIGHT


def is_ball_out():
    if ball_pos_x <= 0 or ball_pos_x >= GRID_WIDTH:
        return True
    else:
        return False


def update_score():
    global score_player_1
    global score_player_2
    if ball_pos_x <= 0:
        score_player_2 += 1
    elif ball_pos_x >= GRID_WIDTH:
        score_player_1 += 1


def reset_ball_pos():
    global ball_pos_x
    global ball_pos_y
    global ball_velocity_x
    ball_pos_x = int(GRID_WIDTH / 2)
    ball_pos_y = int(GRID_HEIGHT / 2)
    ball_velocity_x = -ball_velocity_x


def move_ball():
    global ball_pos_x
    global ball_pos_y
    global ball_velocity_x
    global ball_velocity_y

    # vertical bounds, it doesn't have to check anything else as the ball just bounces off
    ball_pos_y += ball_velocity_y
    if ball_pos_y <= 1:
        ball_pos_y = 1
        ball_velocity_y = -ball_velocity_y
    elif ball_pos_y >= GRID_HEIGHT - 1:
        ball_pos_y = GRID_HEIGHT - 1
        ball_velocity_y = -ball_velocity_y

    # horizontal bounds, it has to check for collision with the paddles as well
    ball_pos_x += ball_velocity_x
    if ball_pos_x <= PADDLE_WIDTH:
        if check_collision():
            ball_pos_x = PADDLE_WIDTH
            ball_velocity_x = -ball_velocity_x
    elif ball_pos_x >= GRID_WIDTH - PADDLE_WIDTH:
        if check_collision():
            ball_pos_x = GRID_WIDTH - PADDLE_WIDTH
            ball_velocity_x = -ball_velocity_x


def check_collision():
    global ball_pos_x
    global ball_pos_y
    global paddle_pos_y

    if ball_pos_x <= PADDLE_WIDTH + 1:
        if paddle_pos_y - PADDLE_HEIGHT < ball_pos_y < paddle_pos_y + PADDLE_HEIGHT:
            return True
        else:
            return False
    elif ball_pos_x >= GRID_WIDTH - PADDLE_WIDTH - 1:
        if paddle_pos_y - PADDLE_HEIGHT < ball_pos_y < paddle_pos_y + PADDLE_HEIGHT:
            return True
        else:
            return False
    return False


def run():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    set_random_velocity()
    global paddle_velocity
    global grid

    while running:
        screen.fill(SCREEN_COLOR)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                running = False
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_w:
                    paddle_velocity = -1
                if i.key == pygame.K_s:
                    paddle_velocity = 1

        move_paddle(paddle_velocity)
        move_ball()
        if is_ball_out():
            update_score()
            reset_ball_pos()
            set_random_velocity()
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
                pygame.draw.circle(screen, BALL_COLOR, (ball_pos_x * SCREEN_RATIO, ball_pos_y * SCREEN_RATIO),
                                   SCREEN_RATIO)

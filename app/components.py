import random
import pygame
from app.globals import *


class Paddle:
    # Paddle position starts as idle, in the middle of the screen
    # It only needs one value for velocity as it can only move vertically
    def __init__(self):
        self.velocity = 0
        self.pos_y = GRID_HEIGHT / 2

    # If the Paddle moves outside the screen, it gets fixed on the border
    # It has to consider the paddle length as well, so it uses PADDLE_HEIGHT instead of 0
    # and GRID_HEIGHT - PADDLE_HEIGHT instead of GRID_HEIGHT
    # The paddle velocity is not reset to 0 after moving, letting the paddle slide
    # moving the paddle by one row in the grid each time would make input really clunky
    def move(self):
        self.pos_y += self.velocity
        if self.pos_y <= PADDLE_HEIGHT - 1:
            self.pos_y = PADDLE_HEIGHT - 1
        elif self.pos_y >= GRID_HEIGHT - PADDLE_HEIGHT:
            self.pos_y = GRID_HEIGHT - PADDLE_HEIGHT


class Ball:
    def __init__(self):
        # The ball is placed at the center of the screen at the start, with a random velocity on both axis
        self.pos_x = int(GRID_WIDTH / 2)
        self.pos_y = int(GRID_HEIGHT / 2)
        self.velocity_x = 0
        self.velocity_y = 0
        self.set_random_velocity()

        # The seeder changes when a paddle hits the ball,
        # so it makes sense to store that information in the ball object
        # and therefore sending it in the same packet.
        # The left paddle starts as the initial seeder
        self.seeder_id = LEFT_PADDLE_ID

    def set_random_velocity(self):
        # velocity on both axis should be either +1 or -1
        if random.choice([True, False]):
            self.velocity_x = 1
        else:
            self.velocity_x = -1

        if random.choice([True, False]):
            self.velocity_y = 1
        else:
            self.velocity_y = -1

    def is_out(self):
        if self.pos_x <= 0 or self.pos_x >= GRID_WIDTH:
            return True
        else:
            return False

    def reset_position(self):
        self.pos_x = int(GRID_WIDTH / 2)
        self.pos_y = int(GRID_HEIGHT / 2)
        self.set_random_velocity()

    # Moves the ball based on the current velocity then checks collisions with paddles
    # and updates the seeder if necessary
    def move(self, left_paddle, right_paddle):
        # vertical bounds, it doesn't have to check anything else as the ball just bounces off
        self.pos_y += self.velocity_y
        if self.pos_y <= 1:
            self.pos_y = 1
            self.velocity_y = -self.velocity_y
        elif self.pos_y >= GRID_HEIGHT - 1:
            self.pos_y = GRID_HEIGHT - 1
            self.velocity_y = -self.velocity_y

        # horizontal bounds, it has to check for collision with the paddles as well
        # if a collision happens, update the seeder
        self.pos_x += self.velocity_x
        if self.pos_x <= PADDLE_WIDTH:
            if self.check_collision_with_paddles(left_paddle, right_paddle):
                self.pos_x = PADDLE_WIDTH
                self.velocity_x = -self.velocity_x
                self.seeder_id = LEFT_PADDLE_ID
        elif self.pos_x >= GRID_WIDTH - PADDLE_WIDTH:
            if self.check_collision_with_paddles(left_paddle, right_paddle):
                self.pos_x = GRID_WIDTH - PADDLE_WIDTH
                self.velocity_x = -self.velocity_x
                self.seeder_id = RIGHT_PADDLE_ID

    # checks for collision with the paddles
    def check_collision_with_paddles(self, left_paddle, right_paddle):
        if self.pos_x <= PADDLE_WIDTH + 1:
            if left_paddle.pos_y - PADDLE_HEIGHT < self.pos_y < left_paddle.pos_y + PADDLE_HEIGHT:
                return True
            else:
                return False
        elif self.pos_x >= GRID_WIDTH - PADDLE_WIDTH - 1:
            if right_paddle.pos_y - PADDLE_HEIGHT < self.pos_y < right_paddle.pos_y + PADDLE_HEIGHT:
                return True
            else:
                return False
        return False


# The Scorekeeper class holds the values of the players' scores
# the display method draws the scores on screen
class Scorekeeper:
    def __init__(self):
        self.score_player_1 = 0
        self.score_player_2 = 0

    def add_score(self, left_paddle_scored):
        if left_paddle_scored:
            self.score_player_1 += 1
        else:
            self.score_player_2 += 1

    def display(self, screen):
        font = pygame.font.SysFont(SCORE_FONT, FONT_SIZE)
        player_a = font.render(str(self.score_player_1), False, TEXT_COLOR)
        screen.blit(player_a, (TEXT_WIDTH_SPACE, TEXT_HEIGHT_SPACE))
        player_b = font.render(str(self.score_player_2), False, TEXT_COLOR)
        screen.blit(player_b, (SCREEN_WIDTH - TEXT_WIDTH_SPACE, TEXT_HEIGHT_SPACE))

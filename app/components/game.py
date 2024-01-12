import sys


def run():
    WIDTH = 100
    HEIGHT = 20
    ball_pos = [50, 10]
    ball_velocity = [0, 0]
    paddle_velocity = 0
    left_paddle = [8, 12]
    right_paddle = [8, 12]
    PADDLE_CHAR = 'x'
    BALL_CHAR = 'o'
    EMPTY_CHAR = ' '

    def move_paddle(paddle, velocity):
        paddle[0] += velocity
        paddle[1] += velocity
        velocity = [0, 0]

    def move_ball(ball, velocity):
        ball[0] += velocity[0]
        ball[1] += velocity[1]

    def print_board():
        for j in range(HEIGHT):
            for i in range(WIDTH):
                if i < 2 and left_paddle[0] < j < left_paddle[1]:
                    print(PADDLE_CHAR, end='')

                elif i > WIDTH - 3 and right_paddle[0] < j < right_paddle[1]:
                    print(PADDLE_CHAR, end='')

                elif i == ball_pos[0] and j == ball_pos[1]:
                    print(BALL_CHAR, end='')

                else:
                    print(EMPTY_CHAR, end='')
            print(EMPTY_CHAR)

    while True:
        key = input()
        if key == 'w':
            # top left is 0, 0 so to go up vertical velocity needs to be -1
            paddle_velocity = -1
        elif key == 's':
            paddle_velocity = 1
        elif key == 'q':
            sys.exit()

        move_paddle(left_paddle, paddle_velocity)
        move_ball(ball_pos, [1, 1])
        print_board()


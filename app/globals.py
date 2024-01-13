# This class is used to store global constants variables
# Python doesn't support actual constants, but using capital letters makes it clear
# that they should not be modified

# Screen sizes of the pygame window
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# The size of the matrix storing the items' positions
# The height is set so that depending on the chosen width the
# aspect ratio is the same as the screen
GRID_WIDTH = 100
GRID_HEIGHT = 56

# The ratio between the screen size and the grid size used to draw the grid on the display
SCREEN_RATIO = 13.66

# The fixed number of frames per second to use for the game
FPS = 60

# Characters used in the 2D matrix that represents the grid
PADDLE_CHAR = 'x'
BALL_CHAR = 'o'
EMPTY_CHAR = ' '

# Colors used by pygame to display the components
SCREEN_COLOR = "black"
BALL_COLOR = "white"
PADDLE_COLOR = "white"
TEXT_COLOR = "white"

# Paddle sizes
PADDLE_HEIGHT = 5
PADDLE_WIDTH = 2

# Score text properties
SCORE_FONT = "Arial"
FONT_SIZE = 100
TEXT_WIDTH_SPACE = int(SCREEN_WIDTH / 4)
TEXT_HEIGHT_SPACE = 100

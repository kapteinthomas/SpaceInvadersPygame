
WIDTH = 600 + 10 # Multpiple of (mob + mobspace) + mobspace 
HEIGHT = 600
FPS = 60

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN = (139 ,69 , 19)

# PLAYER
PLAYER_SPEED = 3
PLAYER_Y_POS = HEIGHT / 8 * 7

# BULLET
BULLET_WIDTH = 5
BULLET_HEIGHT = 20
BULLET_SPEED = 6
BULLET_RATE = 300

# OBSTACLE
OBST_PART_WIDTH = 5
OBST_PART_HEIGHT = 5
OBST_TOTAL_WIDTH = OBST_PART_WIDTH * 10
OBST_TOTAL_HEIGHT = OBST_PART_HEIGHT * 10
NUM_OF_OBSTACLES = 3
OBSTACLE_SPACE = WIDTH / 4


# MOB
MOB_WIDTH = 20
MOB_HEIGHT = 20
MOB_SPACE = 10

MOB_FREE_SPACE = 5
MOBS_COLS = 15
MOBS_ROWS = 4

MOB_FIRE_RATE = 1000
MOB_MOVE_RATE = 1000
# Pygame template - skeleton for a new pygame project
import pygame
import random 
from sprites import *
from settings import *

class Game:
    def __init__(self):
        # initialize pygame and create windowa
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group() 

        # Create player and add to sprites group
        self.player = Player(self)

        # Create mobs and add to sprite group
        self.mob_handler = MobHandler(self, self.player)
        ypos = 10
        xpos = 10
        color = RED
        self.list_of_mobs = []
        row = 1
        for i in range(MOBS_ROWS):
            front_row = False
            col = 1
            if row == MOBS_ROWS:
                front_row = True
                color = YELLOW
            for j in range(MOBS_COLS):
                self.list_of_mobs.append(Mob(self, xpos, ypos, row, col, front_row, color))
                xpos += (MOB_WIDTH + MOB_SPACE)
                col += 1
            ypos += (MOB_HEIGHT + MOB_SPACE)
            xpos = 10
            row += 1

        # Create obstacles
        for k in range(NUM_OF_OBSTACLES):
            startxpos = OBSTACLE_SPACE + (k * OBSTACLE_SPACE) - (OBST_TOTAL_WIDTH / 2)
            ypos = HEIGHT / 8 * 6
            for l in range(int(OBST_TOTAL_HEIGHT / OBST_PART_HEIGHT)):
                if l == 0:
                    ypos = ypos
                else:
                    ypos += OBST_PART_HEIGHT
                xpos = startxpos
                for m in range(int (OBST_TOTAL_WIDTH / OBST_PART_WIDTH)):
                    if m == 0:
                        xpos = xpos
                    else:
                        xpos += OBST_PART_WIDTH
                    obstacle = Obstacle_part(self, xpos, ypos)

        

    def game_loop(self):
        # Game loop
        self.running = True
        while self.running:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            # Update
            self.all_sprites.update()
            self.mob_handler.update()

            pygame.display.set_caption(str(self.clock))

            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            # *after* drawing everything, flip the display
            pygame.display.flip()

        pygame.quit()

    def game_over(self):
        print("Game Over")

game = Game()
game.game_loop()
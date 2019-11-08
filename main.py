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
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont('Arial', 20)
        pygame.display.set_caption("Space Invaders")

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()

        # Create player and add to sprites group
        self.player = Player(self)
        self.score = 0

        # Create mobs and add to sprite group
        self.mob_handler = MobHandler(self, self.player)
        ypos = 25
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

        self.create_HUD()



    def create_HUD(self):
        # Create hearts in HUD
        self.hearts_in_HUD = []
        xheart = WIDTH - 3*(HEART_WIDTH + HEART_SPACE)
        yheart = 100
        for l in range(self.player.lives):
            self.hearts_in_HUD.append(Heart(self, xheart, 0))
            xheart += HEART_WIDTH + HEART_SPACE
    
    def update_HUD(self, lives):
        self.hearts_in_HUD[lives].kill()


    def game_loop(self):
        # Game loop
        running = True
        while running:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)
            for event in pygame.event.get():
                # check for closing window
                if event.type == pygame.QUIT:
                    running = False

            # Update
            self.all_sprites.update()
            self.mob_handler.update()


            # Draw / render
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)

            # Render text
            score_text = "Score: " + str(self.score)
            textsurface = self.game_font.render(score_text, False, (255, 255, 255))
            self.screen.blit(textsurface,(0,0))

            # *after* drawing everything, flip the display
            pygame.display.flip()

        pygame.quit()

    def game_over(self):
        print("Game Over")

game = Game()
game.game_loop()
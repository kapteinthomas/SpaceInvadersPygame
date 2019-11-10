# Pygame template - skeleton for a new pygame project
import pygame, random
from sprites import *
from settings import *
from os import path

class Game:
    def __init__(self):
        # initialize pygame and create windowa
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_font_big = pygame.font.SysFont('Arial', 60)
        self.game_font_mid = pygame.font.SysFont('Arial', 40)
        self.game_font_sml = pygame.font.SysFont('Arial', 20)
        pygame.display.set_caption("Space Invaders")

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()

        # Create player and add to sprites group
        self.game_state = "start"
        self.setup_new_game()
        self.player_name = ""
        self.new_highscore = False
        self.player_beaten = None

    def setup_new_game(self):
        # Setup stuff
        self.player = Player(self)
        self.score = 0
        self.create_mobs()
        self.create_obstacles()
        self.create_HUD()
        self.load_data()
        

    def load_data(self):
        self.dir = path.dirname(__file__)
        f = open(path.join(self.dir, "highscore.txt"), 'r') # Open highscore file for reading
        self.highscores = []
        for line in f.readlines():
            self.highscores.append(line.strip('\n').split(' ')) # strip('\n') is for removing \n from string.
        self.highscore = self.highscores[0][0]
    

    def create_mobs(self):
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


    def create_obstacles(self):
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


    def start_screen(self, event):
        self.screen.fill(BLACK)
        # Headline
        start_text = "SPACE INVADERS!"
        start_surface = self.game_font_big.render(start_text, False, (WHITE))
        # Get rect for centering
        start_rect = start_surface.get_rect(center=(WIDTH/2, 100))
        
        promt_text = "Enter your name"
        promt_surface = self.game_font_mid.render(promt_text, False, (WHITE))
        promt_rect = promt_surface.get_rect(center=(WIDTH/2, 200))
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
            else:
                self.letter = event.unicode
        if event.type == pygame.KEYUP and self.letter:
            self.player_name += self.letter
            self.letter = None
        
        input_surface = self.game_font_mid.render(self.player_name, False, (WHITE))
        input_rect = input_surface.get_rect(center=(WIDTH/2, 300))

        # Blit all text to screen
        self.screen.blit(start_surface,start_rect)
        self.screen.blit(promt_surface, promt_rect)
        self.screen.blit(input_surface, input_rect)



    def game_over_sceen(self):
        self.screen.fill(BLACK)
        start_text = "GAME OVER"
        go_surface = self.game_font_big.render(start_text, False, (WHITE))
        go_rect = go_surface.get_rect(center=(WIDTH/2, 100))
        self.screen.blit(go_surface,go_rect)
        
        if self.new_highscore:
            congrats_text = "Congratulations! You beat " + self.player_beaten + '!'
            congrats_surface = self.game_font_mid.render(congrats_text, False, (GREEN))
            coongrats_rect = congrats_surface.get_rect(center=(WIDTH/2, 160))
            self.screen.blit(congrats_surface, coongrats_rect)

        hs_surface = self.game_font_sml.render("HIGHSCORES", False, (WHITE))
        hs_rect = hs_surface.get_rect(center=(WIDTH/2, 200))
        self.screen.blit(hs_surface, hs_rect)

        # Make list of strings for highscores
        scores = []
        for i in range(len(self.highscores)):
            scores.append(self.highscores[i][0] + '....' + self.highscores[i][1])
        # Make surfaces for bliting
        surfaces = []
        for j in range(len(scores)):
            surfaces.append(self.game_font_sml.render(scores[j], False, (WHITE)))
            rect = surfaces[j].get_rect(center=(WIDTH/2, 220+(50*j)))
            self.screen.blit(surfaces[j], (WIDTH/2, 220+(50*j)))


    def main_screen(self):
        self.all_sprites.update()
        self.mob_handler.update()

        # Draw / render background and sprites
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        # Render text
        score_text = "Score: " + str(self.score)
        score_surface = self.game_font_sml.render(score_text, False, WHITE)
        self.screen.blit(score_surface,(0,0))
        
        namesurface = self.game_font_sml.render(self.player_name, False, WHITE)
        name_rect = namesurface.get_rect(center=(WIDTH/2, 10))
        
        self.screen.blit(namesurface, name_rect)

    
    def game_loop(self):
        # Game loop
        running = True
        while running:
            # keep loop running at the right speed
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if self.game_state == "main":
                self.main_screen()

            elif self.game_state == "start":
                self.start_screen(event)
                # Start game if enter is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_state = "main"
            
            elif self.game_state == "gameover":
                self.game_over_sceen()
                if event.type == pygame.KEYDOWN:
                    self.game_state = "main"
                    self.setup_new_game()

            # *after* drawing everything, flip the display
            pygame.display.flip()

        pygame.quit()


    def end_game(self):
        print("Game Over")
        self.game_state = "gameover"
        #Cleanup
        self.all_sprites.empty()
        self.mobs.empty()
        self.obstacles.empty()
        self.hearts.empty()

        for i in range(len(self.highscores)):
            if self.score > int(self.highscores[i][1]):
                print("Høgere enn " + str((self.highscores[i][0])))
                self.new_highscore = True
                self.player_beaten = self.highscores[i][0]
                new_score_index = i
                break 
        
        if self.new_highscore:
            #move all other scores down and insert new highscore
            if len(self.highscores) < 10:
                self.highscores.append(0) # Just append zero for now, will be filled after
            else:
                self.highscores[9] = 0 # If list is filled, set last item to 0. Will be filled after
            # Bump all items down
            for j in range(len(self.highscores) - 1, new_score_index, -1):
                print(j)
                self.highscores[j] = self.highscores[j-1]
            # Insert new highscore
            self.highscores[new_score_index][1] = str(self.score) # Score
            self.highscores[new_score_index][0] = self.player_name # Name
    




game = Game()
game.game_loop()

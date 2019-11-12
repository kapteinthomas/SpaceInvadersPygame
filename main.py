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
        self.game_font_big = pygame.font.SysFont('monospace', 55)
        self.game_font_mid = pygame.font.SysFont('monospace', 25)
        self.game_font_sml = pygame.font.SysFont('monospace', 20)
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

        self.typing = False

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
        self.highscore = self.highscores[0][1]
        
        self.sound_dir = path.join(self.dir, "sound")
        self.shoot_sound = pygame.mixer.Sound(path.join(self.sound_dir, "pew.wav"))
    

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

    
    def get_txtsurf_and_rect(self, text, font, color, pos):
        surface = font.render(text, False, (color))
        rect = surface.get_rect(center=(pos))
        return (surface, rect)


    def start_screen(self, event):
        self.screen.fill(BLACK)
  
        headline_txt = "SPACE INVADERS!"
        headline = self.get_txtsurf_and_rect(headline_txt, self.game_font_big, WHITE, (WIDTH/2, 100))
        prompt_txt = "Enter your name"
        prompt = self.get_txtsurf_and_rect(prompt_txt, self.game_font_mid, WHITE, (WIDTH/2, 200))

        if event.type == pygame.KEYDOWN and self.typing == False:
            if event.key == pygame.K_BACKSPACE:
                self.player_name = self.player_name[:-1]
                self.typing = True
            else:
                if len(self.player_name) < 10:
                    self.player_name += event.unicode
                    self.typing = True
        if event.type == pygame.KEYUP:
            self.typing = False

        user_input = self.get_txtsurf_and_rect(self.player_name, self.game_font_mid, WHITE, (WIDTH/2, 300))

        # Blit all text to screen
        self.screen.blit(prompt[0], prompt[1])
        self.screen.blit(headline[0], headline[1])
        self.screen.blit(user_input[0], user_input[1])




    def game_over_sceen(self):
        self.screen.fill(BLACK)

        go_txt = self.get_txtsurf_and_rect("GAME OVER", self.game_font_big, WHITE, (WIDTH/2, 100))
        self.screen.blit(go_txt[0], go_txt[1])

        
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
            space = ''
            characters = len(self.highscores[i][0]) + len(str(self.highscores[i][1]))
            for k in range(20 - characters):
                space += '.'
            scores.append(self.highscores[i][0] + space + self.highscores[i][1])
        # Make surfaces for bliting
        surfaces = []
        for j in range(len(scores)):
            surfaces.append(self.game_font_sml.render(scores[j], False, (WHITE)))
            rect = surfaces[j].get_rect(center=(WIDTH/2, 230+(30*j)))
            #self.screen.blit(surfaces[j], (WIDTH/2, 220+(30*j)))
            self.screen.blit(surfaces[j], rect)

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
                # Start game if enter is pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_state = "main"
                else:
                    self.start_screen(event)
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
        #Cleanup the sprite groups
        self.all_sprites.empty()
        self.mobs.empty()
        self.obstacles.empty()
        self.hearts.empty()

        for i in range(len(self.highscores)):
            # Check if score is higher than a score on the scoreboard
            if self.score > int(self.highscores[i][1]):
                print("Higher than " + str((self.highscores[i][0])))
                self.new_highscore = True
                self.player_beaten = self.highscores[i][0]
                new_score_index = i
                break

        if self.new_highscore:
            # Append new score, and sort list.
            self.highscores.append([self.player_name, str(self.score)])
            self.highscores = sorted(self.highscores, key=self.get_score, reverse=True)

    
    def get_score(self, highscore_list):
        return int(highscore_list[1])
    

game = Game()
game.game_loop()

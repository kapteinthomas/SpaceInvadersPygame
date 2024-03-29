import pygame
import random
import time
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.last_shot = 0
        # Set starting position of player
        self.rect.centerx = WIDTH / 2
        self.rect.y = PLAYER_Y_POS
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                centerxpos = self.rect.centerx
                ypos = self.rect.top - BULLET_HEIGHT
                bullet = Bullet(self.game, centerxpos, ypos, 'up')
                self.game.sounds["player_shoot"].play()
    
    def take_damage(self):
        self.game.sounds["hit"].play()
        self.lives -= 1
        if self.lives <= 0:
            self.kill()
            self.game.end_game()
            self.game.sounds["explosion"].play()
    
    def increase_score(self, score):
        self.score += score


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, xpos, ypos, dir):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.y = ypos
        self.dir = dir

    def update(self):
        if self.dir == 'up':
            self.rect.y -= BULLET_SPEED
        if self.dir == 'down':
            self.rect.y += BULLET_SPEED
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.kill()

        # Check for hits with mob
        if self.dir == 'up':    # Only check for 
            hits = pygame.sprite.spritecollide(self, self.game.mobs, True)
            if hits:
                # Stuff for debugging
                col = hits[0].col
                row = hits[0].row
                
                # Find mob object in mob list.
                index_mob_list = self.game.list_of_mobs.index(hits[0])
                # Set mob object one row back as a front mob
                new_front_index = index_mob_list - MOBS_COLS
                if new_front_index < 0:
                    pass
                else:
                    self.game.list_of_mobs[new_front_index].front_row = True
                    self.game.list_of_mobs[new_front_index].image.fill(YELLOW)
                # Printing stuff for debugging
                #print("col: " + str(col) + "\nrow: " + str(row))
                #print("length of mob of list is " + str(len(self.game.list_of_mobs)))
                #print("List item number: " + str(index_mob_list))
                
                # Kill mob that was hit
                self.kill()
                self.game.score += 1
                self.game.sounds["explosion"].play()
                

        # Check for hits with obstacle
        hits_obst = pygame.sprite.spritecollide(self, self.game.obstacles,False)
        if hits_obst:
            self.kill()
            hits_obst[0].kill()
        
        # Check for hits with player
        if pygame.sprite.collide_rect(self, self.game.player):
            self.kill()
            self.game.player.take_damage()
            self.game.update_HUD(self.game.player.lives)


class Obstacle_part(pygame.sprite.Sprite):
    def __init__(self, game, xpos, ypos):
        self.groups = game.all_sprites, game.obstacles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.xpos = xpos
        self.ypos = ypos
        self.image = pygame.Surface((OBST_PART_WIDTH, OBST_PART_HEIGHT))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

class Mob(pygame.sprite.Sprite):
    def __init__(self, game, xpos, ypos, row, col, front_row, color):
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.row = row
        self.col = col
        self.image = pygame.Surface((MOB_WIDTH, MOB_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # Set starting position of mob
        self.rect.x = xpos
        self.rect.y = ypos
        self.front_row = front_row


    def fire(self):
        centerxpos = self.rect.centerx
        ypos = self.rect.bottom + 10
        bullet = Bullet(self.game, centerxpos, ypos, 'down')
        


class MobHandler:
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.time_last_shot = 0
        self.time_last_move = 0
        self.move_direction = 'right'
        self.call_move_down = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.time_last_shot > MOB_FIRE_RATE:
            # Create list of mobs eligble for firing
            mobs_to_fire = []
            for mob in self.game.list_of_mobs:
                if mob.front_row == True:
                    mobs_to_fire.append(mob)
            # Make one random mob from list fire a shot
            # random.choice(mobs_to_fire).fire()
            
            # Make mob closest to player fire
            closest_mob = mobs_to_fire[0]
            smallest_x_diff = abs(closest_mob.rect.x - self.player.rect.centerx)
            for mob in mobs_to_fire:
                # Check difference in x-value
                distance = abs(mob.rect.centerx - self.player.rect.centerx)
                if distance < smallest_x_diff:
                    smallest_x_diff = abs(mob.rect.centerx - self.player.rect.centerx)
                    closest_mob = mob
            closest_mob.fire()
            self.game.sounds["enemy_shot"].play()
            random_float = random.uniform(-2,2)
            self.time_last_shot = now + random_float

        if now - self.time_last_move > MOB_MOVE_RATE:
            self.move()

    def move(self):
        now = pygame.time.get_ticks()
        if self.call_move_down == True:
            self.time_last_move = now
            self.move_down()
            self.call_move_down = False
            return

        if self.move_direction == 'right' and not self.call_move_down:
            for mob in self.game.list_of_mobs:
                mob.rect.x += (MOB_WIDTH + MOB_SPACE)
                if mob.rect.x > WIDTH - (MOB_WIDTH + MOB_SPACE) - 1 and self.call_move_down == False:
                    self.call_move_down = True
                    self.move_direction = 'left'
            self.time_last_move = now
                         
        elif self.move_direction == 'left' and not self.call_move_down:
            for mob in self.game.list_of_mobs:
                mob.rect.x -= (MOB_WIDTH + MOB_SPACE)
                if mob.rect.x < MOB_SPACE + 1 and self.call_move_down == False:
                    self.call_move_down = True
                    self.move_direction = 'right'
            self.time_last_move = now
 

    def move_down(self):
        for mob in self.game.list_of_mobs:
            mob.rect.y += (MOB_WIDTH + MOB_SPACE)
        self.call_move_down = False


class Heart(pygame.sprite.Sprite):
    def __init__(self, game, xpos, ypos):
        self.groups = game.all_sprites, game.hearts
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((HEART_WIDTH, HEART_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
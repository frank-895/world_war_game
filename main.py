import pygame
import math
import random

class plane(object):
    """This class is for all of the planes in the game"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 52
        self.hitbox = (self.x, self.y, 150, 52)

class user_plane(plane):
    """This class is specifically for the user controlled plane"""

    image = pygame.image.load('user_plane.png') # upload main fighter
    heart = pygame.image.load('heart.png') # hearts for lives
    heart = pygame.transform.scale(heart, (30, 30))
    explosion = pygame.image.load('explosion.png')
    explosion = pygame.transform.scale(explosion , (300,300))

    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y) # call superclass init method
        self.velocity = velocity
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) # change plane size
        self.image = pygame.transform.flip(self.image, True, False) # flip image
        self.health = 10
        self.lives = 3
        self.visible = True
        self.gameover = False

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, 150, 52)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2], 10)) # health bar
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2] - ((self.hitbox[2]/10) * (10 - self.health)), 10))
        for i in range(self.lives):
            win.blit(self.heart, (screen_x - 50 - i * 50, 10)) 

    def is_hit(self, bullet):
        """This function determines if the user controlled plane has been hit by a bullet. It removes health and lives if necessary and returns True if user plane is hit"""
        if bullet.x > self.hitbox[0] and bullet.x < self.hitbox[0] + self.hitbox[2]:
            if bullet.y < self.hitbox[1] + self.hitbox[3] and bullet.y > self.hitbox[1]:
                self.health -= 1
                if self.health == 0:
                    self.lost_life()
                    if self.lives == 0:
                        self.no_lives(win)
                return True 
            
    def is_collide(self, enemy):
        """This method determines if the user controlled plane has collided with an enemy plane or the ground"""
        if self.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
            if self.hitbox[0] + self.hitbox[2] > enemy.hitbox[0]:
                if self.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3]:
                    if self.hitbox[1] + self.hitbox[3] > enemy.hitbox[1]:
                        self.lost_life()
        if self.lives == 0:
            self.no_lives(win)
    
    def hit_ground(self):
        """This method determines if the user controlled plane has hit the ground."""
        if self.hitbox[1] + self.hitbox[3] > 700:
            self.lost_life()
            if self.lives == 0:
                self.no_lives(win)

    def lost_life(self):
        self.x = self.y = 100
        self.lives -= 1
        self.health = 10

    def no_lives(self, win):
        win.fill((0,0,0))
        self.gameover = True


class enemy_plane(plane):
    """This class is for enemy planes"""
    
    image = pygame.image.load('enemy_plane.png')
    
    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y)
        self.velocity = velocity
        self.visible = True
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) # change plane size
        self.health = 5
        self.visible = True

    def draw(self, win):
        self.move()
        win.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, 150, 52)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2], 10)) # health bar
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2] - ((self.hitbox[2]/5) * (5 - self.health)), 10)) 

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False   

    def move(self):
        if self.x > -self.width:
            self.x -= self.velocity
        else:
            self.visible = False
            pass # the plane must have made it to the edge of screen - hence game over.

class projectile(object):
    """Class for all projectiles"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)

class bullet(projectile):
    """Class for bullets shot from aircraft"""
    def __init__(self, x, y, direction=1):
        projectile.__init__(self, x, y)
        self.direction = direction
        self.radius = 6
        self.velocity = 15 * self.direction

class bomb(projectile):
    """Class for bombs dropped by aircraft"""
    pass

def is_hit(enemy, bullet):
    """This function determines if a particular bullet has hit a particular enemy plane"""
    if bullet.x > enemy.hitbox[0] and bullet.x < enemy.hitbox[0] + enemy.hitbox[2]:
        if bullet.y < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y > enemy.hitbox[1]:
            return True 

def redraw_game_window():
    """This function redraws the game window between every frame"""
    global scroll
    for i in range(panels):
        win.blit(bg, (i * bg_width + scroll - bg_width, 0))
    
    scroll -= 5
    if abs(scroll) > bg_width:
        scroll = 0

    if main_plane.visible:
        main_plane.draw(win)
    
    for enemy in enemies:
        enemy.draw(win)
        main_plane.is_collide(enemy)
        for bullet in bullets:
            if is_hit(enemy, bullet):
                bullets.pop(bullets.index(bullet))
                enemy.hit()
        if enemy.visible == False:
            enemies.pop(enemies.index(enemy))
    
    for bullet in bullets:
        bullet.draw(win)
    for bullet in enemy_bullets:
        bullet.draw(win)
        if main_plane.is_hit(bullet):
            enemy_bullets.pop(enemy_bullets.index(bullet))

    pygame.display.update()

pygame.init()
screen_x = 2000
screen_y = 800
win = pygame.display.set_mode((screen_x, screen_y)) # creating window
pygame.display.set_caption("World War Game") # creating title
clock = pygame.time.Clock() 
bg = pygame.image.load('inf_background.jpg')
bg_width = bg.get_width()
bg = pygame.transform.scale(bg, (bg_width, screen_y))
bg_rect = bg.get_rect()

scroll = 0
panels = math.ceil(screen_x / bg_width) + 2

enemies = []
main_plane = user_plane(100, 100, 10)
bullets = []
enemy_bullets = []
bullet_limit = 0
enemy_timer = 50
run = True 
score = 0
level1 = True

# main loop
while run:
    

    while level1: 
        clock.tick(27) # frame rate
        main_plane.hit_ground() # check if plane has hit ground each time

        enemy_timer -= 1
        if enemy_timer == 0:
            if len(enemies) < 10:
                enemies.append(enemy_plane(screen_x, random.randint(50, 600), 3))
            enemy_timer = 50

        for enemy in enemies:
            if random.randint(0, 30) == 5:
                enemy_bullets.append(bullet(round(enemy.x + enemy.width), round(enemy.y + enemy.height//2), -1))

        if bullet_limit > 0:
            bullet_limit += 1
        if bullet_limit > 5:
            bullet_limit = 0

        for event in pygame.event.get(): # check for event
            if event.type == pygame.QUIT: # if user closes window
                run = False

        for i in bullets:
            if i.x < screen_x and i.x > 0: # cheeck bullet on screen
                i.x += i.velocity # move the bullet
            else:
                bullets.pop(bullets.index(i))

        for i in enemy_bullets:
            if i.x < screen_x and i.x > 0: # cheeck bullet on screen
                i.x += i.velocity # move the bullet
            else:
                enemy_bullets.pop(enemy_bullets.index(i))

        # For left and right movement of user controlled plane
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and main_plane.x > 0:
            main_plane.x -= main_plane.velocity
        elif keys[pygame.K_RIGHT] and main_plane.x < screen_x - main_plane.width:
            main_plane.x += main_plane.velocity
        
        # For up and down movement of user controlled plane
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and main_plane.y > 0:
            main_plane.y -= main_plane.velocity
        elif keys[pygame.K_DOWN] and main_plane.y < screen_y - main_plane.height:
            main_plane.y += main_plane.velocity

        # For bullet firing of user controlled plane
        if keys[pygame.K_SPACE] and bullet_limit == 0:
            bullets.append(bullet(round(main_plane.x + main_plane.width), round(main_plane.y + main_plane.height//2)))
            bullet_limit = 1

        if score == 10:
            level1 = False

        if main_plane.gameover == True:
            level1 = False
        redraw_game_window()
    
    print("We BROKE out of first while loop!")
    for event in pygame.event.get(): # check for event
            if event.type == pygame.QUIT: # if user closes window
                run = False
    run = False

pygame.quit() # closes program once broken out of while loop

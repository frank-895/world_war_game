import pygame
import math
import random
from pygame import font

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

    def is_hit(self, enemy):
        """This function determines if a particular bullet has hit a particular enemy plane"""
        if self.x > enemy.hitbox[0] and self.x < enemy.hitbox[0] + enemy.hitbox[2]:
            if self.y < enemy.hitbox[1] + enemy.hitbox[3] and self.y > enemy.hitbox[1]:
                return True 
    
class bomb(projectile):
    """Class for bombs dropped by aircraft"""
    pass

def redraw_game_window(score):
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
            if bullet.is_hit(enemy):
                bullets.pop(bullets.index(bullet))
                enemy.hit()
        if enemy.visible == False:
            enemies.pop(enemies.index(enemy))
            score += 1
    
    for bullet in bullets:
        bullet.draw(win)
    for bullet in enemy_bullets:
        bullet.draw(win)
        if main_plane.is_hit(bullet):
            enemy_bullets.pop(enemy_bullets.index(bullet))

    pygame.display.update()

    return score

def every_level():
    """This is the code required for every while loop in the main loop"""
    clock.tick(27) # frame rate
    for event in pygame.event.get(): # check for event
        if event.type == pygame.QUIT: # if user closes window
            return False
    return True

def message(mess, pos):
    """This function is welcome message for each level"""
    global run, intromessage
    run = every_level()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        intromessage = False
    for i in range(panels):
        win.blit(bg, (i * bg_width - bg_width, 0))
        win.blit(bg, (0,0))

    text1 = font.render(mess, True, (0,0,0))
    text2 = font.render("Press space to continue", True, (0,0,0))
    win.blit(text1, (pos, 350))
    win.blit(text2, (800, 450))
    pygame.display.update()

def user_movement(main_plane, screen_x, screen_y, bullets, bullet_limit):
    if bullet_limit > 0:
        bullet_limit += 1
    if bullet_limit > 5:
        bullet_limit = 0
        
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

    return bullet_limit

def move_bullets(bullets):
    for i in bullets:
        if i.x < screen_x and i.x > 0: # cheeck bullet on screen
            i.x += i.velocity # move the bullet
        else:
            bullets.pop(bullets.index(i))
    return bullets



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
level2 = True
level3 = True
intromessage = True  
font = pygame.font.SysFont('comicsans', 45)

# main loop
while run:
    run = every_level()
    
    # THIS IS LEVEL 1
    while level1 and run: 
        run = every_level()  

        # INTROMESSAGE
        while intromessage and level1 and run:
            message("You are defending your airspace alone. You must destroy 10 planes to continue to the next level! Don't let any planes get past!",50)

        main_plane.hit_ground() # check if plane has hit ground each time

        enemy_timer -= 1
        if enemy_timer == 0:
            if len(enemies) < 10:
                enemies.append(enemy_plane(screen_x, random.randint(50, 600), 3))
            enemy_timer = 50

        for enemy in enemies:
            if random.randint(0, 50) == 25:
                enemy_bullets.append(bullet(round(enemy.x + enemy.width), round(enemy.y + enemy.height//2), -1))

        bullets = move_bullets(bullets)
        enemy_bullets = move_bullets(enemy_bullets)
        bullet_limit = user_movement(main_plane, screen_x, screen_y, bullets, bullet_limit)

        if score == 10:
            level1 = False

        if main_plane.gameover == True:
            level1 = False
            level2 = False
        
        score = redraw_game_window(score)

    while level2 and run:
        run = every_level()
        intromessage = True
        while intromessage:
            intromessage = every_level()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                intromessage = False
            for i in range(panels):
                win.blit(bg, (i * bg_width - bg_width, 0))
            win.blit(bg, (0,0))

            text1 = font.render("Congratulations! You made it past the first stage of the game.", True, (0,0,0))
            text2 = font.render("Press space to continue", True, (0,0,0))
            win.blit(text1, (600, 350))
            win.blit(text2, (800, 450))
            
            pygame.display.update()
    
    run = False

pygame.quit() # closes program once broken out of while loop

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

    global gameover

    image = pygame.image.load('user_plane.png') # upload main fighter
    heart = pygame.image.load('heart.png') # hearts for lives
    heart = pygame.transform.scale(heart, (30, 30))

    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y) # call superclass init method
        self.velocity = velocity
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) # change plane size
        self.image = pygame.transform.flip(self.image, True, False) # flip image
        self.health = 10
        self.lives = 3
        self.visible = True

    def draw(self, win):
        """Draws the user plane on the screen"""
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
        gameover = True

class enemy_plane(plane):
    """This class is for enemy planes"""

    global gameover
    
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
            gameover = True

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
        """This method determines if a particular bullet has hit a particular enemy plane"""
        if self.x > enemy.hitbox[0] and self.x < enemy.hitbox[0] + enemy.hitbox[2]:
            if self.y < enemy.hitbox[1] + enemy.hitbox[3] and self.y > enemy.hitbox[1]:
                return True 

class bomb(projectile):
    """Class for bombs dropped by aircraft"""
    pass

def message(mess, pos):
    """This function is welcome message for each level"""
    global intromessage
    intromessage = is_close_window()
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

def is_close_window():
    """This is the code required for every while loop in the main loop"""
    clock.tick(27) # frame rate
    for event in pygame.event.get(): # check for event
        if event.type == pygame.QUIT: # if user closes window
            return False
    return True

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

def enemy_fighter(enemy_timer, enemies, bullet_limit, enemy_bullets):
    enemy_timer -= 1
    if enemy_timer == 0:
        if len(enemies) < 10:
            enemies.append(enemy_plane(screen_x, random.randint(50, 600), 3))
    enemy_timer = 50

    for enemy in enemies:
        if random.randint(0, 50) == 25:
            enemy_bullets.append(bullet(round(enemy.x + enemy.width), round(enemy.y + enemy.height//2), -1))

    if bullet_limit > 0:
        bullet_limit += 1
    if bullet_limit > 5:
        bullet_limit = 0

def move_bullets(bullets, enemy_bullets):
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
   
def user_control():
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

# initialise window
pygame.init()
screen_x = 2000
screen_y = 800
win = pygame.display.set_mode((screen_x, screen_y)) # creating window
pygame.display.set_caption("World War Game") # creating title
clock = pygame.time.Clock() 
font = pygame.font.SysFont('comicsans', 45)

#initialise scrolling background
bg = pygame.image.load('inf_background.jpg')
bg_width = bg.get_width()
bg = pygame.transform.scale(bg, (bg_width, screen_y))
bg_rect = bg.get_rect()
scroll = 0
panels = math.ceil(screen_x / bg_width) + 2

# while loop variables
run = True
levels = [True, True, True]
gameover = False
intromessage = True

# initialise other variables
enemies = []
main_plane = user_plane(100, 100, 10)
bullets = []
enemy_bullets = []
bullet_limit = 0
enemy_timer = 50
score = 0

# main loop
while run:
    run = is_close_window()

    while levels[0] and not gameover:
        levels[0] = is_close_window()
        
        while intromessage:
            intromessage = is_close_window()
        message("You are defending your airspace alone. You must destroy 10 planes to continue to the next level! Don't let any planes get past!",50)
        enemy_fighter(enemy_timer, enemies, bullet_limit, enemy_bullets)
        move_bullets(bullets, enemy_bullets)
        user_control()
        
        
        if score == 10:
            level1 = False

        if gameover == True:
            level1 = False
            level2 = False
        
        score = redraw_game_window(score)

    #while levels[1] and not gameover:
    #    levels[1] = is_close_window()

    #while levels[2] and not gameover:
    #    levels[2] = is_close_window()

    #if gameover == False:
    #    pass
    #else:
    #    pass
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
        self.hitbox = (self.x, self.y, self.width, self.height)

class user_plane(plane):
    """This class is specifically for the user controlled plane"""

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
        self.gameover = False

    def draw(self, win, is_shield):
        win.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, 150, 52)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2], 10)) # health bar
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2] - ((self.hitbox[2]/10) * (10 - self.health)), 10))
        for i in range(self.lives):
            win.blit(self.heart, (screen_x - 50 - i * 50, 10)) 
        if is_shield:
            pygame.draw.ellipse(win, (0,0,255), (self.x, self.y, self.width, self.height), 2)

    def is_hit(self, bullet):
        """This function determines if the user controlled plane has been hit by a bullet. It removes health and lives if necessary and returns True if user plane is hit"""
        if bullet.x > self.hitbox[0] and bullet.x < self.hitbox[0] + self.hitbox[2]:
            if bullet.y < self.hitbox[1] + self.hitbox[3] and bullet.y > self.hitbox[1]:
                if not is_shield:
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
    
    global run
    image = pygame.image.load('enemy_plane.png')
    
    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y)
        self.velocity = velocity
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) # change plane size
        self.health = 5
        self.visible = True

    def draw(self, win):
        self.move()
        win.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
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
            main_plane.gameover = True
            run = False

class projectile(object):
    """Class for all projectiles"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)

    def is_hit(self, enemy):
        """This function determines if a particular bullet has hit a particular enemy"""
        if self.x > enemy.hitbox[0] and self.x < enemy.hitbox[0] + enemy.hitbox[2]:
            if self.y < enemy.hitbox[1] + enemy.hitbox[3] and self.y > enemy.hitbox[1]:
                return True 

class bullet(projectile):
    """Class for bullets shot from airplanes and tanks"""
    def __init__(self, x, y, direction=1, angle=0):
        projectile.__init__(self, x, y)
        self.direction = direction
        self.angle = angle
        self.radius = 6
        self.velocity = 15 * self.direction
            
    def move(self):
        if self.x < screen_x and self.x > 0: # check bullet on screen
                self.x += self.velocity # move the bullet
                if self.y < screen_y and self.y > 0:
                    self.y -= self.velocity * self.angle
                    return True
        else:
            return False
    
class bomb(projectile):
    """Class for bombs dropped by aircraft"""
    def __init__(self, x, y):
        projectile.__init__(self,x,y)
        self.radius = 13
        self.velocity = 20

    def move(self):
        if self.y < 700: # check bomb hasn't hit ground
            self.y += self.velocity # move bomb downwards
            return True
        else:
            return False

class tank(object):
    """This class is for the tanks that enter in the second level"""
    global enemy_bullets

    image = pygame.image.load("tank.png")

    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.width = 130
        self.height = 80
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.velocity = 3 * facing
        self.image_left = pygame.transform.scale(self.image, (self.width, self.height))
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.visible = True
        if self.facing == 1:
            self.path = [self.x, screen_x//2]
        else:
            self.path = [screen_x//2, self.x]

    def draw(self, win):
        self.move()
        if self.velocity > 0:
            win.blit(self.image_right, (self.x, self.y))
        else:
            win.blit(self.image_left, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)

    def hit(self):
        self.visible = False

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.facing = -self.facing
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.facing = -self.facing
    
    def fire(self):
        if self.facing == 1:
            enemy_bullets.append(bullet(round(self.x + self.width), round(self.y), self.facing, self.facing*.3))
        else:
            enemy_bullets.append(bullet(round(self.x), round(self.y), self.facing, self.facing*.3))
                    
class blimp(object):
    """This class is for the boss in the final level"""
    
    global run
    image = pygame.image.load('blimp.png')

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 600
        self.height = 200
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.velocity = 10
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.initial_health = 50
        self.health = self.initial_health
        self.visible = True

    def draw(self, win):
        self.move()
        win.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 15, self.width, 10)) # health bar
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 15, self.width - ((self.width/self.initial_health) * (self.initial_health - self.health)), 10)) 
        if self.x < screen_x - self.width:
            self.velocity = 0.5

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
            run = False
            main_plane.gameover = True
    
    def fire(self):            
        enemy_bullets.append(bullet(round(self.x), round(self.y + self.height//2), -1, 0))
        enemy_bullets.append(bullet(round(self.x), round(self.y + self.height//2), -1, .3))
        enemy_bullets.append(bullet(round(self.x), round(self.y + self.height//2), -1, -.3))

class message(object):
    """This class is for any messages that will appear on the screen"""

    def __init__(self):
        self.width = 1200
        self.height = 700
        self.button_height = 200
        self.button_width = 210
        self.home = pygame.transform.scale(pygame.image.load('home.JPG'), (self.width, self.height))
        self.home_play = pygame.transform.scale(pygame.image.load('home_play_hover.JPG'), (self.width, self.height))
        self.home_exit = pygame.transform.scale(pygame.image.load('home_exit_hover.JPG'), (self.width, self.height))
        self.level2 = pygame.transform.scale(pygame.image.load('level2.JPG'), (self.width, self.height))
        self.level2_play = pygame.transform.scale(pygame.image.load('level2_play_hover.JPG'), (self.width, self.height))
        self.level2_exit = pygame.transform.scale(pygame.image.load('level2_exit_hover.JPG'), (self.width, self.height))
        self.level3 = pygame.transform.scale(pygame.image.load('level3.JPG'), (self.width, self.height))
        self.level3_play = pygame.transform.scale(pygame.image.load('level3_play_hover.JPG'), (self.width, self.height))
        self.level3_exit = pygame.transform.scale(pygame.image.load('level3_exit_hover.JPG'), (self.width, self.height))
        self.lost = pygame.transform.scale(pygame.image.load('lost.JPG'), (self.width, self.height))
        self.lost_play = pygame.transform.scale(pygame.image.load('lost_play_hover.JPG'), (self.width, self.height))
        self.lost_exit = pygame.transform.scale(pygame.image.load('lost_exit_hover.JPG'), (self.width, self.height))
        self.won = pygame.transform.scale(pygame.image.load('won.JPG'), (self.width, self.height))
        self.won_play = pygame.transform.scale(pygame.image.load('won_play_hover.JPG'), (self.width, self.height))
        self.won_exit = pygame.transform.scale(pygame.image.load('won_exit_hover.JPG'), (self.width, self.height))
        self.left_button_box = (450, 260, self.button_width, self.button_height)
        self.right_button_box = (1340, 260, self.button_width, self.button_height)

    def screen_message(self, win, image, image_left_hover, image_right_hover):
        global run
        (x,y) = pygame.mouse.get_pos()

        if x > self.left_button_box[0] and x < self.left_button_box[0] + self.left_button_box[2] and y < self.left_button_box[1] + self.left_button_box[3] and y > self.left_button_box[3]:
            win.blit(image_left_hover, (400,50))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return False
                
        elif x > self.right_button_box[0] and x < self.right_button_box[0] + self.right_button_box[2] and y < self.right_button_box[1] + self.right_button_box[3] and y > self.right_button_box[3]:
            win.blit(image_right_hover, (400,50))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        else:
            win.blit(image, (400, 50))

        pygame.display.update()
        return True

class collectible(object):
    """For user special abilities"""
    def __init__(self, x, y):
        self.radius = 30
        self.width = 30
        self.height = 30
        self.x = x
        self.y = y
        self.hitbox = (self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        self.visible = True

    def draw(self, icon, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius, 2)
        win.blit(icon, (self.x - 15, self.y - 15))
        if self.is_collected():
            if self.activate(win):
                return True

    def is_collected(self):
        """This function determines if the collectible has been collected"""
        if self.hitbox[0] < main_plane.hitbox[0] + main_plane.hitbox[2]:
            if self.hitbox[0] + self.hitbox[2] > main_plane.hitbox[0]:
                if self.hitbox[1] < main_plane.hitbox[1] + main_plane.hitbox[3]:
                    if self.hitbox[1] + self.hitbox[3] > main_plane.hitbox[1]:
                        self.visible = False
                        return True
                
class extra_life(collectible):

    heart = pygame.image.load('heart.png') # hearts for lives

    def __init__(self, x, y):
        collectible.__init__(self, x, y)
        self.icon = pygame.transform.scale(self.heart, (self.width, self.height))
    
    def activate(self, win):
        main_plane.lives += 1

class shield(collectible):
    shield = pygame.image.load("sheild.png") # load in image for icon

    def __init__(self, x, y):
        collectible.__init__(self, x, y)
        self.icon = pygame.transform.scale(self.shield, (self.width, self.height))

    def activate(self, win):
        global is_shield, counter  
        is_shield = True
        counter = 0

class rapid_fire(collectible):
    
    bullet_icon = pygame.image.load('bullet.png')

    def __init__(self, x, y):
        collectible.__init__(self, x, y)
        self.icon = pygame.transform.scale(self.bullet_icon, (self.width, self.height))

    def activate(self, win):
        global is_rapid_fire, counter
        is_rapid_fire = True
        counter = 0

def redraw_game_window(score):
    """This function redraws the game window between every frame"""
    global scroll, is_shield, counter, is_rapid_fire
    for i in range(panels):
        win.blit(bg, (i * bg_width + scroll - bg_width, 0))
    scroll -= 5
    if abs(scroll) > bg_width:
        scroll = 0

    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (50,50))

    if main_plane.visible:
        main_plane.draw(win, is_shield)
    
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
    for i in bombs:
        i.draw(win)

    try:
        for i in tanks:
            i.draw(win)
            for j in bombs:
                if j.is_hit(i):
                    bombs.pop(bombs.index(j))
                    i.hit()
            if i.visible == False:
                score += 1
                if i.x > screen_x//2:
                    i.x = screen_x + i.width
                else: 
                    i.x = -i.width
                i.visible = True
    except Exception:
        pass

    try:
        if boss.visible:
            boss.draw(win)
            for i in bullets:
                if i.is_hit(boss):
                    bullets.pop(bullets.index(i))
                    boss.hit()
                if boss.visible == False:
                    score = 1 # Game Over
    except Exception:
        pass

    for i in collectibles:
        i.draw(i.icon, win)
        if not i.visible:
            collectibles.pop(collectibles.index(i))
    if is_shield or is_rapid_fire:
        counter += 1
    if counter == 500:
        is_shield = False
        is_rapid_fire = False
    
    pygame.display.update()

    return score

def every_level():
    """This is the code required for every while loop in the main loop"""
    clock.tick(27) # frame rate
    for event in pygame.event.get(): # check for event
        if event.type == pygame.QUIT: # if user closes window
            return False
    return True   

def user_movement(main_plane, screen_x, screen_y, bullets, bullet_limit, bombs, bomb_limit):
    global level1

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

    if keys[pygame.K_w] and bomb_limit == 0 and not level1:
        bombs.append(bomb(round(main_plane.x + main_plane.width//2), round(main_plane.y + main_plane.height)))
        bomb_limit = 1

    return (bullet_limit, bomb_limit)

def produce_enemy():
    global enemy_timer, enemies, enemy_bullets, screen_x, tanks, bullet_timer, bullet_limit, bomb_limit, boss_cooldown, stop
    
    if bullet_limit > 0:
        bullet_limit += 1
    if bullet_limit > 5 or (bullet_limit > 3 and is_rapid_fire):
        bullet_limit = 0
        
    if bomb_limit > 0:
        bomb_limit += 1
    if bomb_limit > 20:
        bomb_limit = 0

    boss_cooldown += 1
    if boss_cooldown > 2:
        boss_cooldown = 0

    stop += 1
    if stop > 60:
        stop = 0
    
    enemy_timer -= 1
    if enemy_timer == 0:
        if len(enemies) < 10:
            if level2 == True:
                enemies.append(enemy_plane(screen_x, random.randint(50, 600), 3))
            else:
                temp = random.randint(50,600)
                while temp > 300 and temp < 500:
                    temp = random.randint(50,600)
                enemies.append(enemy_plane(screen_x, temp, 3))
        enemy_timer = 50

    for enemy in enemies:
        if random.randint(0, 50) == 25:
            enemy_bullets.append(bullet(round(enemy.x), round(enemy.y + enemy.height//2), -1))     

    if random.randint(0,10) == 5:
        try:
            for i in tanks:
                i.fire()
        except Exception:
            pass

    if boss_cooldown and stop < 30:
        try:
            boss.fire()
        except Exception:
            pass

def set_up_variables():
    global enemies, bullets, enemy_bullets, bullet_limit, enemy_timer, score, intromessage, bombs, bomb_limit, boss_cooldown, stop, collectibles, is_shield, is_rapid_fire, counter
    enemies = []
    bullets = []
    bombs = []
    enemy_bullets = []
    collectibles = []
    bullet_limit = 0
    bomb_limit = 0
    enemy_timer = 50
    score = 0
    boss_cooldown = 0
    stop = 0
    is_shield = False
    is_rapid_fire = False
    counter = 0

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
font = pygame.font.SysFont('comicsans', 45) # set up text for game

scroll = 0
panels = math.ceil(screen_x / bg_width) + 2

main_plane = user_plane(100, 100, 10)
set_up_variables()
level1 = True
level2 = True
level3 = True
intromessage = True
run = True 
message_obj = message()
collectibles = [rapid_fire(400,100)]

# main loop
while run:
    run = every_level()
    
    # THIS IS LEVEL 1
    while level1 and run: 
        run = every_level()  

        # INTROMESSAGE        
        while intromessage and level1 and run:
            run = every_level()

            for i in range(panels):
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0,0))

            intromessage = message_obj.screen_message(win, message_obj.home, message_obj.home_play, message_obj.home_exit)
            pygame.display.update()

        main_plane.hit_ground() # check if plane has hit ground each time
        produce_enemy()

        for i in bullets:
            if i.move() == False:
                bullets.pop(bullets.index(i))
        for i in enemy_bullets:
            if i.move() == False:
                enemy_bullets.pop(enemy_bullets.index(i))
        (bullet_limit, bomb_limit) = user_movement(main_plane, screen_x, screen_y, bullets, bullet_limit, bombs, bomb_limit)

        if score == 2:
            level1 = False

        if main_plane.gameover == True:
            level1 = False
            level2 = False
            level3 = False
        
        score = redraw_game_window(score)

    set_up_variables()
    intromessage = True
    main_plane.x = 100
    main_plane.y = 100
    main_plane.health = 10
    main_plane.lives = 3
    tanks = [tank(-130, 700, 1), tank(2000, 700, -1)]

    # THIS IS LEVEL 2
    while level2 and run:
        run = every_level()

        # INTROMESSAGE
        while intromessage and level2 and run:
            run = every_level()

            for i in range(panels):
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0,0))

            intromessage = message_obj.screen_message(win, message_obj.level2, message_obj.level2_play, message_obj.level2_exit)
            pygame.display.update()

        main_plane.hit_ground() # check if plane has hit ground each time
        produce_enemy()
        for i in bullets:
            if i.move() == False:
                bullets.pop(bullets.index(i))
        for i in enemy_bullets:
            if i.move() == False:
                enemy_bullets.pop(enemy_bullets.index(i))
        for i in bombs:
            if i.move() == False:
                bombs.pop(bombs.index(i))
        (bullet_limit, bomb_limit) = user_movement(main_plane, screen_x, screen_y, bullets, bullet_limit, bombs, bomb_limit)

        if score == 2:
            level2 = False

        if main_plane.gameover == True:
            level2 = False
            level3 = False
        
        score = redraw_game_window(score)
        
    set_up_variables()
    intromessage = True
    main_plane.x = 100
    main_plane.y = 100
    main_plane.health = 10
    main_plane.lives = 3
    tanks = [tank(-130, 700, 1), tank(2000, 700, -1)]
    boss = blimp(2000, 300)
    bullet_timer = 0 

    # THIS IS LEVEL 3
    while level3 and run:
        run = every_level()

        # INTROMESSAGE
        while intromessage and level3 and run:
            run = every_level()

            for i in range(panels):
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0,0))

            intromessage = message_obj.screen_message(win, message_obj.level3, message_obj.level3_play, message_obj.level3_exit)
            pygame.display.update()

        main_plane.hit_ground() # check if plane has hit ground each time
        produce_enemy()
        for i in bullets:
            if i.move() == False:
                bullets.pop(bullets.index(i))
        for i in enemy_bullets:
            if i.move() == False:
                enemy_bullets.pop(enemy_bullets.index(i))
        for i in bombs:
            if i.move() == False:
                bombs.pop(bombs.index(i))
        (bullet_limit, bomb_limit) = user_movement(main_plane, screen_x, screen_y, bullets, bullet_limit, bombs, bomb_limit)

        if score == 100 or boss.visible == False:
            level3 = False

        if main_plane.gameover == True:
            level3 = False
        
        score = redraw_game_window(score)

    if main_plane.gameover == True:
        intromessage = True
        while intromessage and run:
            run = every_level()

            for i in range(panels):
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0,0))

            intromessage = message_obj.screen_message(win, message_obj.lost, message_obj.lost_play, message_obj.lost_exit)
            pygame.display.update()
    else:
        intromessage = True
        while intromessage and run:
            run = every_level()

            for i in range(panels):
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0,0))

            intromessage = message_obj.screen_message(win, message_obj.won, message_obj.won_play, message_obj.won_exit)
            pygame.display.update()

    if intromessage == False:
        main_plane.x = 100
        main_plane.y = 100
        main_plane.health = 10
        main_plane.lives = 3
        main_plane.gameover = False
        set_up_variables()
        level1 = True
        level2 = True
        level3 = True
        run = True 
        message_obj = message()
        tanks = []
        boss = []

pygame.quit() # closes program once broken out of while loop
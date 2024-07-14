import pygame
import math
import random


class plane(object):
    """This class is for all of the planes in the game"""

    def __init__(self, x, y):
        self.x = x  # x and y coordinates mark position
        self.y = y
        self.width = 150  # to resize images
        self.height = 52
        # to determine if plane has been hit
        self.hitbox = (self.x, self.y, self.width, self.height)


class user_plane(plane):
    """This class is specifically for the user controlled plane"""

    image = pygame.image.load('images/user_plane.png')  # upload main fighter
    heart = pygame.image.load('images/heart.png')  # hearts for lives
    heart = pygame.transform.scale(heart, (30, 30))  # rescale heart image

    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y)  # call superclass init method
        self.velocity = velocity  # defines plane's speed
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))  # change plane size
        self.image = pygame.transform.flip(
            self.image, True, False)  # flip image
        self.health = 10  # for health bar
        self.lives = 3  # once health bar depletes, life will be lost
        self.visible = True  # to determine if plane should be displayed
        self.gameover = False  # determines if game has been lost

    def draw(self, win, is_shield):
        """This function draws the user controlled plane onto the screen as well as health bars, lives and shields"""
        win.blit(self.image, (self.x, self.y)
                 )  # blit the main plane on window at its x and y coordinates
        self.hitbox = (self.x, self.y, self.width,
                       self.height)  # redefine hit box
        pygame.draw.rect(
            # health bar
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2], 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2] - (
            (self.hitbox[2]/10) * (10 - self.health)), 10))
        for i in range(self.lives):  # display lives with icon
            win.blit(self.heart, (screen_x - 50 - i * 50, 10))
        if is_shield:  # if shield collectible has been activated draw shield
            pygame.draw.ellipse(
                win, (0, 0, 255), (self.x, self.y, self.width, self.height), 2)

    def is_hit(self, bullet):
        """This function determines if the user controlled plane has been hit by a bullet. It removes health and lives if necessary and returns True if user plane is hit"""
        if bullet.x > self.hitbox[0] and bullet.x < self.hitbox[0] + self.hitbox[2]:
            if bullet.y < self.hitbox[1] + self.hitbox[3] and bullet.y > self.hitbox[1]:
                if not is_shield:  # no damage if shielf activated
                    self.health -= 1
                if self.health == 0:  # if health depleted life is lost
                    self.lost_life()
                    if self.lives == 0:  # if all lives lost, game = lost
                        self.no_lives(win)
                return True  # so the program knows to remove bullet from the game

    def is_collide(self, enemy):
        """This method determines if the user controlled plane has collided with an enemy plane or the ground"""
        if self.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
            if self.hitbox[0] + self.hitbox[2] > enemy.hitbox[0]:
                if self.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3]:
                    if self.hitbox[1] + self.hitbox[3] > enemy.hitbox[1]:
                        self.lost_life()  # if two planes collide, the user immediatley loses a life
        if self.lives == 0:  # check if game has been lost
            self.no_lives(win)

    def hit_ground(self):
        """This method determines if the user controlled plane has hit the ground."""
        if self.hitbox[1] + self.hitbox[3] > 700:  # ground is at 700 pixels
            self.lost_life()
            if self.lives == 0:  # check if game has been lost
                self.no_lives(win)

    def lost_life(self):
        """Method activated every time life is lost"""
        self.x = self.y = 100  # respawn plane in original location
        self.lives -= 1  # remove lief
        self.health = 10  # reinstate health if life lost

    def no_lives(self, win):
        """Method activated if game is lost as user loses all lives"""
        win.fill((0, 0, 0))  # remove all images from window
        self.gameover = True  # mark game as over


class enemy_plane(plane):
    """This class is for specifically enemy planes"""

    global run  # to mark if necessary to cut out of main loop
    image = pygame.image.load('images/enemy_plane.png')

    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y)  # call superclass method
        self.velocity = velocity  # speed of enemy
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))  # change image size
        self.health = 5  # for health bar
        self.visible = True  # to make enemy plane dissapear if it loses all of its health

    def draw(self, win):
        """To draw enemy plane and its health bar on window"""
        self.move()  # every time enemy drawn it needs to be moved
        win.blit(self.image, (self.x, self.y))  # blit image on screen
        # redefine hitbox every time plane moves
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(
            # health bar
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2], 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 15, self.hitbox[2] - (
            (self.hitbox[2]/5) * (5 - self.health)), 10))

    def hit(self):
        """Method activated every time enemy plane hit by user"""
        if self.health > 1:
            self.health -= 1  # remove health
        else:  # plane has no health left
            self.visible = False

    def move(self):
        """Method moves plane every screen refresh"""
        if self.x > -self.width:  # once plane has reached end of screen game is over
            self.x -= self.velocity  # move plane according to velocity
        else:
            self.visible = False  # plane dissapears
            main_plane.gameover = True  # mark game as over
            run = False  # break our of main loop


class projectile(object):
    """Class for all projectiles"""

    def __init__(self, x, y):
        self.x = x  # to mark its x and y coordinate on the window
        self.y = y

    def draw(self, win):
        """Method called every screen refresh to draw bullet on window"""
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)

    def is_hit(self, enemy):
        """This function determines if a particular bullet has hit a particular enemy"""
        if self.x > enemy.hitbox[0] and self.x < enemy.hitbox[0] + enemy.hitbox[2]:
            if self.y < enemy.hitbox[1] + enemy.hitbox[3] and self.y > enemy.hitbox[1]:
                return True  # bullet has hit enemy


class bullet(projectile):
    """Class for bullets shot from all vessels"""

    def __init__(self, x, y, direction=1, angle=0):
        projectile.__init__(self, x, y)
        self.direction = direction  # to determine which direction the bullet is fired in
        self.angle = angle  # angle is a multiple by which the x coordinate will be multiplied
        self.radius = 6  # radius of bullet
        # bullets move at velocity 15, and in the same direction as the vessel that shot it
        self.velocity = 15 * self.direction

    def move(self):
        """Method redraws bullet each time screen refreshes"""
        if self.x < screen_x and self.x > 0:  # check bullet on screen
            self.x += self.velocity  # move the bullet in the horizontal direction
            if self.y < screen_y and self.y > 0:  # check bullet on screen
                self.y -= self.velocity * self.angle  # move bullet in vertical direction
                return True
        else:
            return False


class bomb(projectile):
    """Class for bombs dropped by aircraft"""

    def __init__(self, x, y):
        projectile.__init__(self, x, y)
        self.radius = 13  # radius of bomb
        self.velocity = 20  # velocity of bomb

    def move(self):
        """Method moves bomb each screen refresh"""
        if self.y < 700:  # check bomb hasn't hit ground
            self.y += self.velocity  # move bomb downwards
            return True
        else:  # bomb has hit ground
            return False


class tank(object):
    """This class is for the tanks that enter in the second level"""
    global enemy_bullets

    # image displayed to represent tank
    image = pygame.image.load("images/tank.png")

    def __init__(self, x, y, facing):
        self.x = x  # x and y coordinates to mark position on window
        self.y = y
        self.facing = facing  # to determine which way tank is moving
        self.width = 130  # width of tank image
        self.height = 80  # height of tank image
        # to determine if tank has been hit by a projectile
        self.hitbox = (self.x, self.y, self.width, self.height)
        # velocity multiplied by facing to ensure it moves in correct direction
        self.velocity = 3 * facing
        self.image_left = pygame.transform.scale(
            self.image, (self.width, self.height))  # left version of image
        self.image_right = pygame.transform.flip(
            self.image_left, True, False)  # right version is flipped
        self.visible = True  # to determine if tank must dissapear as it has been hit
        if self.facing == 1:  # the path the tank will move along
            self.path = [self.x, screen_x//2]
        else:
            self.path = [screen_x//2, self.x]

    def draw(self, win):
        """Redraw tank each time screen refreshes"""
        self.move()  # move tank each time it is blitted on screen
        if self.velocity > 0:  # blit right image if moving right
            win.blit(self.image_right, (self.x, self.y))
        else:  # blit left image if moving left
            win.blit(self.image_left, (self.x, self.y))
        # redefine hitbox each time the tank moves
        self.hitbox = (self.x, self.y, self.width, self.height)

    def hit(self):
        """Method activated if tank is hit by bomb"""
        self.visible = False

    def move(self):
        """Method to move tank between each screen refresh"""
        if self.velocity > 0:  # if tank moving right
            # check if tank has reached edge of path
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:  # if tank has reached edge of screen change its velocity and direction it is facing
                self.velocity = self.velocity * -1
                self.facing = -self.facing
        else:  # if tank moving left
            # check if tank has reached edge of path
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:  # if tank has reached edge of screen change its velocity and direction it is facing
                self.velocity = self.velocity * -1
                self.facing = -self.facing

    def fire(self):
        """Method to fire bullets from tank"""
        if self.facing == 1:  # place relative to tank the bullet originates depends on which direction it is facing
            enemy_bullets.append(
                bullet(round(self.x + self.width), round(self.y), self.facing, self.facing*.3))
        else:
            enemy_bullets.append(bullet(round(self.x), round(
                self.y), self.facing, self.facing*.3))


class blimp(object):
    """This class is for the boss in the final level"""

    global run  # variable breaks main loop if user exits
    # upload icon to represent blimp
    image = pygame.image.load('images/blimp.png')

    def __init__(self, x, y):
        self.x = x  # to mark x and y coordinates
        self.y = y
        self.width = 600  # width of blimp
        self.height = 200  # height of blimp
        # to determine if blimp is hit with user bullet
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.velocity = 10  # initial speed of blimp
        # resize image to match widthand height variables
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.initial_health = 100  # boss has lots of health
        self.health = self.initial_health  # health will be dimished as blimp is hit
        self.visible = True  # to mark if blimp has been destroyed

    def draw(self, win):
        """Method redraws blimp on window each time it is destroyed"""
        self.move()  # move blimp each time it is redrawn
        win.blit(self.image, (self.x, self.y))  # blit blimp on window
        # redefine hitbox each time it moves
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(
            # health bar
            win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 15, self.width, 10))
        pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 15, self.width - (
            (self.width/self.initial_health) * (self.initial_health - self.health)), 10))
        if self.x < screen_x - self.width:  # change velocity once blimp is complelety visible on screen
            self.velocity = 0.5

    def hit(self):
        """Method activated each time blimp is hit with bullet"""
        if self.health > 1:  # check blimp hasn't run out of health
            self.health -= 1
        else:  # if no health left, mark as destroyed
            self.visible = False

    def move(self):
        """Method moves the blimp between each screen refresh"""
        if self.x > -self.width:  # check blimp hasn't reached edge of screen
            self.x -= self.velocity  # moves blimp
        else:
            self.visible = False  # mark blimp as invisible if it reaches edges of screen
            run = False  # break out of main loop
            main_plane.gameover = True  # to show the game has been lost

    def fire(self):
        """To fire bullets from three turrets"""
        enemy_bullets.append(bullet(round(self.x), round(
            self.y + self.height//2), -1, 0))  # horizontal fire
        enemy_bullets.append(bullet(round(self.x), round(
            self.y + self.height//2), -1, .3))  # sligthly upward angled fire
        enemy_bullets.append(bullet(round(self.x), round(
            self.y + self.height//2), -1, -.3))  # sligthly downward angled fire


class message(object):
    """This class is for any messages that will appear on the screen"""

    def __init__(self):
        self.width = 1200  # width of message box
        self.height = 700  # height of message box
        self.button_height = 200  # height and width of the buttons
        self.button_width = 210
        # hitboxes for left and right buttons
        self.left_button_box = (
            450, 260, self.button_width, self.button_height)
        self.right_button_box = (
            1340, 260, self.button_width, self.button_height)
        # for each different message, there is a version for if the left button has been hovered over or right button has been hovered over
        self.home = pygame.transform.scale(pygame.image.load(
            'images/home.JPG'), (self.width, self.height))
        self.home_play = pygame.transform.scale(pygame.image.load(
            'images/home_play_hover.JPG'), (self.width, self.height))
        self.home_exit = pygame.transform.scale(pygame.image.load(
            'images/home_exit_hover.JPG'), (self.width, self.height))
        self.level2 = pygame.transform.scale(pygame.image.load(
            'images/level2.JPG'), (self.width, self.height))
        self.level2_play = pygame.transform.scale(pygame.image.load(
            'images/level2_play_hover.JPG'), (self.width, self.height))
        self.level2_exit = pygame.transform.scale(pygame.image.load(
            'images/level2_exit_hover.JPG'), (self.width, self.height))
        self.level3 = pygame.transform.scale(pygame.image.load(
            'images/level3.JPG'), (self.width, self.height))
        self.level3_play = pygame.transform.scale(pygame.image.load(
            'images/level3_play_hover.JPG'), (self.width, self.height))
        self.level3_exit = pygame.transform.scale(pygame.image.load(
            'images/level3_exit_hover.JPG'), (self.width, self.height))
        self.lost = pygame.transform.scale(pygame.image.load(
            'images/lost.JPG'), (self.width, self.height))
        self.lost_play = pygame.transform.scale(pygame.image.load(
            'images/lost_play_hover.JPG'), (self.width, self.height))
        self.lost_exit = pygame.transform.scale(pygame.image.load(
            'images/lost_exit_hover.JPG'), (self.width, self.height))
        self.won = pygame.transform.scale(pygame.image.load(
            'images/won.JPG'), (self.width, self.height))
        self.won_play = pygame.transform.scale(pygame.image.load(
            'images/won_play_hover.JPG'), (self.width, self.height))
        self.won_exit = pygame.transform.scale(pygame.image.load(
            'images/won_exit_hover.JPG'), (self.width, self.height))

    def screen_message(self, win, image, image_left_hover, image_right_hover):
        """Method displays particular message on screen"""

        events = pygame.event.get()  # to see if user presses the mouse down
        global run  # to break out of main loop if user presses exit
        (x, y) = pygame.mouse.get_pos()  # x and y coordinate of cursor

        # check if cursor in button hitbox
        if x > self.left_button_box[0] and x < self.left_button_box[0] + self.left_button_box[2] and y < self.left_button_box[1] + self.left_button_box[3] and y > self.left_button_box[3]:
            win.blit(image_left_hover, (400, 50))  # blit button hover image
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return False  # if play button pressed break out of message loop

        # check if cursor in button hitbox
        elif x > self.right_button_box[0] and x < self.right_button_box[0] + self.right_button_box[2] and y < self.right_button_box[1] + self.right_button_box[3] and y > self.right_button_box[3]:
            win.blit(image_right_hover, (400, 50))  # blit button hover image
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False  # if exit button pressed break out of main loop

        else:  # if not hovering over either button show neutral message image
            win.blit(image, (400, 50))

        pygame.display.update()  # update window display manually
        return True


class collectible(object):
    """For user special abilities"""

    def __init__(self, x, y):
        self.radius = 30  # radius of collectible
        self.width = 50  # width and height of icon
        self.height = 50
        self.x = x  # x and y coordinate of collectible
        self.y = y
        # to determine if collectible has been collected
        self.hitbox = (self.x - self.radius, self.y -
                       self.radius, self.radius * 2, self.radius * 2)
        self.visible = True  # mark as invisble if collected

    def draw(self, icon, win):
        """Method to redraw collectible image on screen between each refresh"""
        pygame.draw.circle(win, (0, 0, 0), (self.x, self.y),
                           self.radius, 2)  # blit circle border
        # blit icon in the centre of circle
        win.blit(icon, (self.x - 25, self.y - 25))
        if self.is_collected():
            if self.activate(win):  # if collected activate collectible
                return True  # to remove collectible from collectibles list

    def is_collected(self):
        """This method determines if the collectible has been collected"""
        if self.hitbox[0] < main_plane.hitbox[0] + main_plane.hitbox[2]:
            if self.hitbox[0] + self.hitbox[2] > main_plane.hitbox[0]:
                if self.hitbox[1] < main_plane.hitbox[1] + main_plane.hitbox[3]:
                    # determines if plane has entered hitbox of collectible
                    if self.hitbox[1] + self.hitbox[3] > main_plane.hitbox[1]:
                        self.visible = False  # mark collectible as invisible if collected
                        return True


class extra_life(collectible):
    """This collectible gives player an extra life"""
    heart = pygame.image.load('images/heart.png')  # for icon

    def __init__(self, x, y):
        collectible.__init__(self, x, y)  # call initialisation of superclass
        self.icon = pygame.transform.scale(
            self.heart, (self.width, self.height))  # resize icon

    def activate(self, win):
        """Method determines the change that occurs if collectible collected"""
        main_plane.lives += 1  # if activated give extra life to player


class shield(collectible):
    """This collectible prevents damage for player"""
    shield = pygame.image.load("images/sheild.png")  # load in image for icon

    def __init__(self, x, y):
        collectible.__init__(self, x, y)  # call initialisation of superclass
        self.icon = pygame.transform.scale(
            self.shield, (self.width, self.height))

    def activate(self, win):
        """Method determines the change that occurs if collectible collected"""
        global is_shield, counter
        is_shield = True  # if activated mark shield activated
        counter = 0  # timer to stop shield after certain time


class rapid_fire(collectible):
    """"This collectible allows player to fire bullets more rapidly"""
    bullet_icon = pygame.image.load('images/bullet.png')

    def __init__(self, x, y):
        collectible.__init__(self, x, y)  # call initialisation of superclass
        self.icon = pygame.transform.scale(
            self.bullet_icon, (self.width, self.height))

    def activate(self, win):
        """Method determines the change that occurs if collectible collected"""
        global is_rapid_fire, counter
        is_rapid_fire = True  # if activated mark rapid fire activated
        counter = 0  # timer to stop rapid fire after certain time


def redraw_game_window(score):
    """This function redraws the game window between every frame"""
    global scroll, is_shield, counter, is_rapid_fire  # variables that need to outlast the function

    # for scrolling background
    for i in range(panels):
        win.blit(bg, (i * bg_width + scroll - bg_width, 0))
    scroll -= 5
    if abs(scroll) > bg_width:
        scroll = 0

    text = font.render('Score: ' + str(score), 1,
                       (0, 0, 0))  # display score to user
    win.blit(text, (50, 50))  # blit score on screen

    if main_plane.visible:
        # draw user controlled plane if it hasn't been destroyed
        main_plane.draw(win, is_shield)

    for enemy in enemies:  # iterate through all enemies
        enemy.draw(win)  # draw each enemy
        # check if main_plane has collided with each enemy
        main_plane.is_collide(enemy)
        for bullet in bullets:  # for each bullet and each enemy check if bullet has hit enemy
            if bullet.is_hit(enemy):
                # if enemy hit, remove bullet from list
                bullets.pop(bullets.index(bullet))
                enemy.hit()  # activate hit function if enemy hit
        if enemy.visible == False:  # don't display enemy if destroyed
            # remove enemy from list if destroyed
            enemies.pop(enemies.index(enemy))
            score += 1  # increase score each time enemy is destroyed

    for bullet in bullets:  # blit each bullet on screen
        bullet.draw(win)

    for bullet in enemy_bullets:  # blit each enemy bullet on screen
        bullet.draw(win)
        # for each enemy bullet check if user has been hit. is_hit contains necessary changes to user if user is hit
        if main_plane.is_hit(bullet):
            # if user is hit remove enemy bullet from list
            enemy_bullets.pop(enemy_bullets.index(bullet))

    for i in bombs:
        i.draw(win)  # draw each bomb on screen. moved in draw() method.
    try:  # first level no tanks, try prevents error
        for i in tanks:
            i.draw(win)  # blit tank on screen
            for j in bombs:
                if j.is_hit(i):  # for each tank and each bomb check if tank is hit
                    bombs.pop(bombs.index(j))  # remove bomb if it hits tank
                    i.hit()  # activate tank hit method if it is hit
            if i.visible == False:  # if tank is destroyed
                score += 1  # increase user score
                if i.x > screen_x//2:  # respawn tank depending which path it was on
                    i.x = screen_x + i.width
                else:
                    i.x = -i.width
                i.visible = True  # make tank visible again, but respawned in original location
    except Exception:  # during first level
        pass

    try:  # first and second level no blimp, try prevents error
        if boss.visible:
            boss.draw(win)  # blit blimp if visible
            for i in bullets:  # for each user bullet
                if i.is_hit(boss):  # check if boss is hit
                    # if bullet hits, make it dissapear
                    bullets.pop(bullets.index(i))
                    boss.hit()  # activate boss hit method
                if boss.visible == False:  # if boss is destroyed game over
                    score = 100
    except Exception:  # during first level
        pass

    for i in collectibles:  # for each collectible
        i.draw(i.icon, win)  # blit icon on screen
        if not i.visible:  # if collected remove from collectibles list
            collectibles.pop(collectibles.index(i))
    if is_shield or is_rapid_fire:  # increase timer for each collectible
        counter += 1
    if counter == 300:  # once timer is completed mark abilities as inactive
        is_shield = False
        is_rapid_fire = False

    pygame.display.update()  # update screen manually each screen refresh

    return score  # to update score for main loop


def every_level():
    """This is the code required for every while loop in the main loop"""
    clock.tick(27)  # frame rate
    for event in pygame.event.get():  # check for event
        if event.type == pygame.QUIT:  # if user closes window
            return False
    return True


def user_movement(main_plane, screen_x, screen_y, bullets, bombs, is_rapid_fire):
    """This function is moves the user controlled plane depdning on user keyboard inputs"""

    global level1, bullet_limit, bomb_limit  # so variables outlast the function

    if bullet_limit > 0:  # to prevent bullet firing being too fast
        bullet_limit += 1
    # timer is shorter when rapid fire is active
    if bullet_limit > 5 or (bullet_limit > 3 and is_rapid_fire):
        bullet_limit = 0

    if bomb_limit > 0:  # to prevent bomb firing being too fast
        bomb_limit += 1
    if bomb_limit > 20:
        bomb_limit = 0

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
        bullets.append(bullet(round(main_plane.x + main_plane.width),
                       round(main_plane.y + main_plane.height//2)))
        bullet_limit = 1  # to prevent rapid fire

    # for bomb firing of user controlled plane
    if keys[pygame.K_w] and bomb_limit == 0 and not level1:  # no bombs in first level
        bombs.append(bomb(round(main_plane.x + main_plane.width//2),
                     round(main_plane.y + main_plane.height)))
        bomb_limit = 1


def produce_enemy():
    """This function produces the enemies in each level and the projectiles they fire"""
    global enemy_timer, enemies, enemy_bullets, screen_x, tanks, boss_cooldown, stop  # so variables outlast function

    boss_cooldown += 1  # fire rate of boss
    if boss_cooldown > 2:
        boss_cooldown = 0

    stop += 1  # to have gaps between firing of boss
    if stop > 60:
        stop = 0

    enemy_timer -= 1  # to make enemies appear at regular intervals
    if enemy_timer == 0:
        if len(enemies) < 10:  # maximum of 10 enemy planes at a time
            if level2 == True:  # first and second level enemy planes can spawn anywhere
                enemies.append(enemy_plane(
                    screen_x, random.randint(50, 600), 3))
            else:  # third level enemy planes cannot spawn where boss is
                temp = random.randint(50, 600)
                while temp > 300 and temp < 500:
                    temp = random.randint(50, 600)
                enemies.append(enemy_plane(screen_x, temp, 3))
        enemy_timer = 50  # reset timer each time enemy spawns

    for enemy in enemies:
        if random.randint(0, 50) == 25:  # 1 in 50 chance of enemy firing bullet
            enemy_bullets.append(bullet(round(enemy.x), round(
                enemy.y + enemy.height//2), -1))  # enemy plane fires

    if random.randint(0, 10) == 5:  # 1 in 10 chance of tank firing bullet
        try:  # no tanks in first level, try prevents error
            for i in tanks:  # all tanks fire in unison
                i.fire()  # tank fires
        except Exception:  # in case no tanks
            pass

    if boss_cooldown and stop < 30:
        try:  # no boss in first or second levels, try prevents error
            boss.fire()
        except Exception:  # in case no boss
            pass


def set_up_variables():
    """This function resets all the variables that are the same for each level"""
    global enemies, bullets, enemy_bullets, bullet_limit, enemy_timer, score, intromessage, bombs, bomb_limit, boss_cooldown, stop, collectibles, is_shield, is_rapid_fire, counter, collectibles  # so variables outlast function
    enemies = []  # to store enemy planes
    bullets = []  # to store user bullets
    bombs = []  # to store user bombs
    enemy_bullets = []  # to store enemy bullets
    collectibles = []  # to store visible collectibles
    bullet_limit = 0  # user bullet timer
    bomb_limit = 0  # user bomb timer
    enemy_timer = 50  # enemy plane respawn timer
    score = 0  # to mark number of destroyed enemies
    boss_cooldown = 0  # fire rate of boss
    stop = 0  # breaks between boss bullet firing
    is_shield = False  # mark if shield collectible activated
    is_rapid_fire = False  # mark is rapid fire collectible activated
    counter = 0  # timer for collectibles
    collectibles = []  # to store collectibles visisble on screen


pygame.init()  # initialise pygame
screen_x = 2000  # screen size
screen_y = 800
win = pygame.display.set_mode((screen_x, screen_y))  # creating window
pygame.display.set_caption("World War Game")  # creating title
clock = pygame.time.Clock()  # create game clock
bg = pygame.image.load('images/inf_background.jpg')  # load in background image
bg_width = bg.get_width()  # get background width
# make background correct height
bg = pygame.transform.scale(bg, (bg_width, screen_y))
bg_rect = bg.get_rect()  # get rectangle coordinates of background
font = pygame.font.SysFont('comicsans', 45)  # set up text for game

scroll = 0  # multiple for scrolling background
panels = math.ceil(screen_x / bg_width) + 2  # number of panels of background

main_plane = user_plane(100, 100, 10)  # create user controlled plane variable
set_up_variables()  # set up variables prior to first level
level1 = True  # to keep each levels loop going until user completes it or loses
level2 = True
level3 = True
intromessage = True  # to keep message on screen until user presses play
run = True  # to mark if main loop needs to keep running, to False this variable is to exit game
message_obj = message()  # to make message methods run

# MAIN LOOP
while run:
    run = every_level()  # with clock and close window code

    # THIS IS LEVEL 1
    while level1 and run:  # only runs while level1 and run is True
        run = every_level()  # with clock and close window code

        # INTROMESSAGE
        while intromessage and level1 and run:  # if main loop broken or level1 broken, break out of loop
            run = every_level()  # with clock and close window code

            for i in range(panels):  # background while message is displayed
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0, 0))

            intromessage = message_obj.screen_message(
                # display first level message
                win, message_obj.home, message_obj.home_play, message_obj.home_exit)
            pygame.display.update()  # manually refresh window display

        main_plane.hit_ground()  # check if plane has hit ground each time
        produce_enemy()  # to make enemy planes appear

        for i in bullets:
            if i.move() == False:  # move user bullets
                # and remove if they make impact or reach edge of screen
                bullets.pop(bullets.index(i))
        for i in enemy_bullets:
            if i.move() == False:  # move enemy bullets
                # and remove if they make impact or reach edge of screen
                enemy_bullets.pop(enemy_bullets.index(i))
        user_movement(main_plane, screen_x, screen_y, bullets,
                      bombs, is_rapid_fire)  # to allow user to move planee

        # 1 in 500 chance of new collectible appearing, and no more than one at a time
        if random.randint(0, 500) == 100 and not collectibles:
            # randomly choose collectible to appear
            choice = random.randint(0, 2)
            if choice == 0:
                collectibles.append(extra_life(
                    random.randint(50, 1000), random.randint(50, 700)))
            elif choice == 1:
                collectibles.append(rapid_fire(
                    random.randint(50, 1000), random.randint(50, 700)))
            else:
                collectibles.append(
                    shield(random.randint(50, 1000), random.randint(50, 700)))

        if score == 20:  # user has passed level if they score 20
            level1 = False

        if main_plane.gameover == True:  # if user loses, break all level loops
            level1 = False
            level2 = False
            level3 = False

        score = redraw_game_window(score)  # manually refresh window

    set_up_variables()  # restate variables for new level
    intromessage = True  # for new message
    main_plane.x = 100  # respawn user in original location
    main_plane.y = 100
    main_plane.health = 10  # refresh user health and lives
    main_plane.lives = 3
    # new variable for this level - tanks
    tanks = [tank(-130, 700, 1), tank(2000, 700, -1)]

    # THIS IS LEVEL 2
    while level2 and run:
        run = every_level()  # with clock and close window code

        # INTROMESSAGE
        while intromessage and level2 and run:  # if main loop broken or level2 broken, break out of loop
            run = every_level()  # with clock and close window code

            for i in range(panels):  # background while message is displayed
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0, 0))

            intromessage = message_obj.screen_message(
                # display second level message
                win, message_obj.level2, message_obj.level2_play, message_obj.level2_exit)
            pygame.display.update()  # manually refresh window display

        main_plane.hit_ground()  # check if plane has hit ground each time
        produce_enemy()  # to make enemy planes and tanks appear
        for i in bullets:
            if i.move() == False:  # move user bullets
                # and remove if they make impact or reach edge of screen
                bullets.pop(bullets.index(i))
        for i in enemy_bullets:
            if i.move() == False:  # move enemy bullets
                # and remove if they make impact or reach edge of screen
                enemy_bullets.pop(enemy_bullets.index(i))
        for i in bombs:
            if i.move() == False:  # move user bombs
                # and remove if impact made or hit ground
                bombs.pop(bombs.index(i))
        user_movement(main_plane, screen_x, screen_y, bullets,
                      bombs, is_rapid_fire)  # allow user to move plane

        # 1 in 500 chance of new collectible appearing, and no more than one at a time
        if random.randint(0, 500) == 100 and not collectibles:
            # randomly choose collectible to appear
            choice = random.randint(0, 2)
            if choice == 0:
                collectibles.append(extra_life(
                    random.randint(50, 1000), random.randint(50, 700)))
            elif choice == 1:
                collectibles.append(rapid_fire(
                    random.randint(50, 1000), random.randint(50, 700)))
            else:
                collectibles.append(
                    shield(random.randint(50, 1000), random.randint(50, 700)))

        if score == 20:  # user has passed level if they score 20
            level2 = False

        if main_plane.gameover == True:  # if user loses, break all level loops
            level2 = False
            level3 = False

        score = redraw_game_window(score)  # manually refresh window

    set_up_variables()  # restate variables for new level
    intromessage = True  # for new intro message
    main_plane.x = 100  # respawn user in original location
    main_plane.y = 100
    main_plane.health = 10  # reinstate user health and lives
    main_plane.lives = 3
    tanks = [tank(-130, 700, 1), tank(2000, 700, -1)]  # tanks for level 3
    boss = blimp(2000, 300)  # create boss object for final level

    # THIS IS LEVEL 3
    while level3 and run:  # only runs while level3 and run is True
        run = every_level()  # with clock and close window code

        # INTROMESSAGE
        while intromessage and level3 and run:  # if main loop broken or level1 broken, break out of loop
            run = every_level()  # with clock and close window code

            for i in range(panels):  # background while message is displayed
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0, 0))

            intromessage = message_obj.screen_message(
                # display third level message
                win, message_obj.level3, message_obj.level3_play, message_obj.level3_exit)
            pygame.display.update()  # manually refresh window display

        main_plane.hit_ground()  # check if plane has hit ground each time
        produce_enemy()  # to make enemy planes, tanks and boss appear
        for i in bullets:
            if i.move() == False:  # move user bullets
                # and remove if they make impact or reach edge of screen
                bullets.pop(bullets.index(i))
        for i in enemy_bullets:
            if i.move() == False:  # move enemy bullets
                # and remove if they make impact or reach edge of screen
                enemy_bullets.pop(enemy_bullets.index(i))
        for i in bombs:
            if i.move() == False:  # move user bombs
                # and remove if they make impact or reach edge of screen
                bombs.pop(bombs.index(i))
        user_movement(main_plane, screen_x, screen_y, bullets,
                      bombs, is_rapid_fire)  # to allow user to move planee

        # 1 in 500 chance of new collectible appearing, and no more than one at a time
        if random.randint(0, 500) == 100 and not collectibles:
            # randomly choose collectible to appear
            choice = random.randint(0, 2)
            if choice == 0:
                collectibles.append(extra_life(
                    random.randint(50, 1000), random.randint(50, 700)))
            elif choice == 1:
                collectibles.append(rapid_fire(
                    random.randint(50, 1000), random.randint(50, 700)))
            else:
                collectibles.append(
                    shield(random.randint(50, 1000), random.randint(50, 700)))

        if boss.visible == False:  # user passes if they destroy the boss
            level3 = False

        if main_plane.gameover == True:  # if user loses, break all level loops
            level3 = False

        score = redraw_game_window(score)  # manually refresh window

    if main_plane.gameover == True:  # if user loses
        intromessage = True  # to allow new message to display
        while intromessage and run:  # run will break loop if user presses close
            run = every_level()  # with clock and close window code

            for i in range(panels):  # background while message is displayed
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0, 0))

            intromessage = message_obj.screen_message(
                # display "you lost" message
                win, message_obj.lost, message_obj.lost_play, message_obj.lost_exit)
            pygame.display.update()  # manually refresh window display
    else:  # if user hasn't lost they've won
        intromessage = True  # to allow new message to display
        while intromessage and run:  # run will break loop if user closes window
            run = every_level()  # with clock and close window code

            for i in range(panels):  # background while message is displayed
                win.blit(bg, (i * bg_width - bg_width, 0))
                win.blit(bg, (0, 0))

            intromessage = message_obj.screen_message(
                # display "you won" message
                win, message_obj.won, message_obj.won_play, message_obj.won_exit)
            pygame.display.update()  # manually refresh window display

    if intromessage == False:  # if user presses retry all variables have to reinstated
        main_plane.x = 100  # respawn in original location
        main_plane.y = 100
        main_plane.health = 10  # fresh lives and health
        main_plane.lives = 3
        main_plane.gameover = False  # game restarts so gameover false
        set_up_variables()  # reinstate the variables that are the same in every level
        level1 = True  # for each level loop
        level2 = True
        level3 = True
        run = True  # to allow user to close window and break out of loop completely
        message_obj = message()  # to use message methods
        tanks = []  # no tanks in first level
        boss = []  # no boss in first level

pygame.quit()  # closes program once broken out of while loop

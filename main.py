import pygame

class plane(object):
    """This class is for all of the planes in the game"""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 52

class user_plane(plane):
    """This class is specifically for the user controlled plane"""

    image = pygame.image.load('user_plane.png') # upload main fighter

    def __init__(self, x, y, velocity):
        plane.__init__(self, x, y) # call superclass init method
        self.velocity = velocity
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) # change plane size
        self.image = pygame.transform.flip(self.image, True, False) # flip image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


def redraw_game_window():
    """This function redraws the game window between every frame"""
    win.blit(bg, (0,0))
    main_plane.draw(win)
    pygame.display.update()

pygame.init()
screen_x = 2000
screen_y = 1100
win = pygame.display.set_mode((screen_x, screen_y)) # creating window
pygame.display.set_caption("World War Game") # creating title
clock = pygame.time.Clock() 
bg = pygame.image.load('bg.jpg')
bg = pygame.transform.scale(bg, (screen_x, screen_y))

main_plane = user_plane(100, 100, 20)
run = True # main loop
while run:
    clock.tick(27) # frame rate

    for event in pygame.event.get(): # check for event
        if event.type == pygame.QUIT: # if user closes window
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and main_plane.x > 0:
        main_plane.x -= main_plane.velocity
    elif keys[pygame.K_RIGHT] and main_plane.x < screen_x - main_plane.width:
        main_plane.x += main_plane.velocity
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and main_plane.y > 0:
        main_plane.y -= main_plane.velocity
    elif keys[pygame.K_DOWN] and main_plane.y < screen_y - main_plane.height:
        main_plane.y += main_plane.velocity
    
    redraw_game_window()

pygame.quit() # closes program once broken out of while loop

import pygame

pygame.init()
screen_x = 1500
screen_y = 1100
win = pygame.display.set_mode((screen_x, screen_y)) # creating window
pygame.display.set_caption("World War Game") # creating title
clock = pygame.time.Clock() 

run = True # main loop
while run:
    clock.tick(27) # frame rate

    for event in pygame.event.get(): # check for event
        if event.type == pygame.QUIT: # if user closes window
            run = False

pygame.quit() # closes program once broken out of while loop

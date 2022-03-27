from cgi import test
import pygame
import game_settings as gs
from block import Block
#Initialising PyGame
pygame.init()

#Creating the pygame screen
screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
game_running = True

#Array to keep track of all the blocks in the world
workd_blocks = []


#main game loop:
while game_running:
    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            game_running = False
    screen.fill('white')



    pygame.display.update()



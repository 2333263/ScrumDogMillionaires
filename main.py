import pygame
import game_settings as gs
from level_generator import getBlocks 
#Initialising PyGame
pygame.init()

#Creating the pygame screen
screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
game_running = True

#Array to keep track of all the blocks in the world
world_blocks = getBlocks("level")

#main game loop:
while game_running:
    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            game_running = False
    #Create the sky 
    screen.fill(gs.customColours["sky"])

    for block in world_blocks:
        screen.blit(block, block.blockPosition)

    pygame.display.update()
    

    



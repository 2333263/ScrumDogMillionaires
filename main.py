import pygame
import game_settings as gs
from level_generator import getBlocks
import math
import break_place_handler as bph
#Initialising PyGame
pygame.init()

#Creating the pygame screen
screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
game_running = True

#Array to keep track of all the blocks in the world
world_blocks = getBlocks(gs.level_name)

#main game loop:
while game_running:
    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            game_running = False

        #Logic for player interaction

        #1 -- left click
        #2 -- middle click
        #3 -- right click
        #4 -- scroll up
        #5 -- scroll down
        if events.type == pygame.MOUSEBUTTONDOWN:
            if events.button == 1:
                break_block = bph.block_break(pygame.mouse.get_pos(),world_blocks)
    
            if events.button == 3:
                #Returns X,Y relative to block size !!! NOT PYGAME COORDS !!!
                pos = math.floor(pygame.mouse.get_pos()[0]/gs.block_size),math.floor(pygame.mouse.get_pos()[1]/gs.block_size)
                

        
    #Create the sky 
    screen.fill(gs.customColours["sky"])

    for block in world_blocks:
        screen.blit(block, block.blockPosition)

    pygame.display.update()
    

    


import pygame
import game_settings as gs
from level_generator import getBlocks
import break_place_handler as bph
import inventory_handler as inv
import player_movement as pm
#Initialising PyGame
pygame.init()

#Creating the pygame screen
screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
game_running = True

#Array to keep track of all the blocks in the world
world_blocks = getBlocks(gs.level_name)

player=pm.Player((0,gs.height/8),gs.block_size,(0,0,0))
player.update(world_blocks)

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
            #Will add tool checks after each event.button check for effeciency, and other aspects (when we get there)
            if events.button == 1:
                bph.block_break(pygame.mouse.get_pos(),world_blocks) #break the block
                
            elif events.button == 3:
                bph.block_place(pygame.mouse.get_pos(),world_blocks) #place the block

            #Scroll UP to select next item in hotbar
            elif events.button == 4:
                inv.select_next()

            #Scroll DOWN to select previous item in hotbar
            elif events.button == 5:
                inv.select_previous()

    if(events.type==pygame.KEYUP):
        player.StopMoveOnX()
    elif(events.type==pygame.KEYDOWN):
        player.MoveOnX()
    player.update(world_blocks)      
     
   
    #Create the sky 
    screen.fill(gs.customColours["Sky"])

    for block in world_blocks:
        screen.blit(block, block.blockPosition)

    screen.blit(player.image,(player.rect.x,player.rect.y))
    pygame.display.update()

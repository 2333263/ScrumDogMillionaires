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

#initilize a player object with attributes, position (x,y) and size (horizontal size, verical size is 2x horizontal)
player=pm.Player((100,gs.height/8),gs.block_size)

#main game loop:
while game_running:
    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            game_running = False

        # Logic for player interaction
        # 1 -- left click
        # 2 -- middle click
        # 3 -- right click
        # 4 -- scroll up
        # 5 -- scroll down
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
             #if a key is pressed and that key is the up arrow, run the jump method in the player class
        elif(events.type==pygame.KEYDOWN):
            if(events.key==pygame.K_UP or events.key==pygame.K_SPACE):
                player.jump()
    #runs the move on X which checks if the player is pressing an arrow key to move
    player.MoveOnX()
    #update the player position
    player.update(world_blocks)      
     
   
    #Create the sky 
    screen.fill(gs.customColours["Sky"])

    for block in world_blocks:
        screen.blit(block, block.blockPosition)
    #blits the player to the screen based on the location of the player
    screen.blit(player.image,(player.rect.x,player.rect.y))
    
    #VERY TEMPORARY, here to make the placing easier when debugging itemIDs 
    #Create a font that displays the current block and count, also create a rectangle to draw the font to
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('Block Selected: ' + gs.itemIDs[inv.selected] + ' : ' + str(inv.get_selected().getCount()), True, "white")
    textRect = text.get_rect()
    textRect.center = (4.5 * gs.block_size, gs.block_size)
    
    #Create the sky 
    screen.fill(gs.colorNames["Sky"])

    #Draw all the created blocks to the screen 
    for block in world_blocks:
        current_block = pygame.image.load("Tiles/" + block.textureName)
        current_block = pygame.transform.scale(current_block, (gs.block_size, gs.block_size))
        screen.blit(current_block, block.blockPosition)

    
    screen.blit(text, textRect)
    pygame.display.update()

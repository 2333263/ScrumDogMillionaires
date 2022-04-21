import pygame
import gameSettings as gs
from levelGenerator import getBlocks
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerHandler as ph
import CraftingMenu as cm


#Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()

#Creating the pygame screen
screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
gameRunning = True

#Array to keep track of all the blocks in the world
worldBlocks = getBlocks(gs.levelName)


#initilize a player object with attributes, position (x,y) and size (horizontal size, verical size is 2x horizontal)
player = ph.Player((gs.width/2 - gs.blockSize * 4, gs.height/3), gs.blockSize)

#Initialise the crafting table screen 
crafter = cm.Crafting(screen)

#main game loop:
while gameRunning:
    clock.tick(60) #Sets the frame to update 60 times a second

    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            gameRunning = False

        # Logic for player interaction
        # 1 -- left click
        # 2 -- middle click
        # 3 -- right click
        # 4 -- scroll up
        # 5 -- scroll down
        if events.type == pygame.MOUSEBUTTONDOWN:
            #Will add tool checks after each event.button check for effeciency, and other aspects (when we get there)
            if events.button == 1:
                bph.blockBreak(pygame.mouse.get_pos(), worldBlocks, player) #break the block
                crafter.checkClick(pygame.mouse.get_pos())
            elif events.button == 3:
                bph.blockPlace(pygame.mouse.get_pos(), worldBlocks, player) #place the block
                
            #Scroll UP to select next item in hotbar
            elif events.button == 4:
                inv.selectNext()

            #Scroll DOWN to select previous item in hotbar
            elif events.button == 5:
                inv.selectPrevious()


        #if a key is pressed and that key is the up arrow, run the jump method in the player class
        elif(events.type==pygame.KEYDOWN):
            if(events.key==pygame.K_UP or events.key==pygame.K_SPACE):
                player.jump()


    #runs the move on X which checks if the player is pressing an arrow key to move
    player.MoveOnX()
    #update the player position
    player.update(clock.tick(), worldBlocks)


    #VERY TEMPORARY, here to make the placing easier when debugging itemIDs 
    #Create a font that displays the current block and count, also create a rectangle to draw the font to
    font = pygame.font.Font('Minecraft.ttf', 16)
    text = font.render('Block Selected: ' + gs.itemIDs[inv.selected] + ' : ' + str(inv.getSelected().getCount()), True, "white")
    textRect = text.get_rect()
    textRect.center = (4.5 * gs.blockSize, gs.blockSize)
    #add a frame rate counter to top right corner
    text2 = font.render("FPS: "+str(int(clock.get_fps())), 1, (0, 0, 0))

    #Create the sky 
    #screen.fill(gs.colorNames["Sky"])
    
    bg = pygame.image.load(gs.textureNames["Sky"]).convert()
    bg = pygame.transform.scale(bg, (gs.width, gs.height))
    screen.blit(bg, (0, 0))

    #Draw all the created blocks to the screen
    worldBlocks.draw(screen)

    #blits the player to the screen based on the location of the player
    screen.blit(text, textRect)
    screen.blit(text2, (gs.width - 100, 5))

    screen.blit(player.image, (player.rect.x, player.rect.y))

    if(gs.drawCrafting):
        crafter.makeScreen()
        #crafter.populateRecipe(11).draw(screen)
    

    #Finally update the  screen with all the above changes     
    pygame.display.update()

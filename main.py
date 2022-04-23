import pygame
import gameSettings as gs
from levelGenerator import getBlocks
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerHandler as ph
import Camera as cam
import CraftingMenu as cm

#Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()

#Creating the pygame screen

screen = pygame.display.set_mode((gs.blockSize*gs.noXBlocks, gs.blockSize*gs.noYBlocks))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
gameRunning = True

#Array to keep track of all the blocks in the world
worldBlocks = getBlocks(gs.levelName)
collisionblocks=worldBlocks #list of blocks player can collide with, initially entire world but updated within first time step

#initilize a player object with attributes, position (x,y) and size (horizontal size, verical size is 2x horizontal)
player = ph.Player((gs.width/2 - gs.blockSize * 4, gs.height/3), gs.blockSize)
camera=cam.Camera(player)

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
                bph.blockBreak(pygame.mouse.get_pos()+camera.getOffsets(), worldBlocks, player) #break the block
                crafter.checkClick(pygame.mouse.get_pos()) #MIGHT NEED TO ADD OFFSET
                crafter.makeItem(pygame.mouse.get_pos())
            elif events.button == 3:
                bph.blockPlace(pygame.mouse.get_pos()+camera.getOffsets(), worldBlocks, player) #place the block
                
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
    player.update(clock.tick(),  collisionblocks)


    #VERY TEMPORARY, here to make the placing easier when debugging itemIDs 
    #Create a font that displays the current block and count, also create a rectangle to draw the font to
    font = pygame.font.Font('Minecraft.ttf', 16)
   # text = font.render('Block Selected: ' + gs.itemIDs[inv.selected] + ' : ' + str(inv.getSelected().getCount()), True, "white")
    #textRect = text.get_rect()
    #textRect.center = (4.5 * gs.blockSize, gs.blockSize)
    #add a frame rate counter to top right corner
    fpsText = font.render("FPS: "+str(int(clock.get_fps())), 1, (0, 0, 0))

    #Create the sky 
    #screen.fill(gs.colorNames["Sky"])
    
    bg = pygame.image.load(gs.textureNames["Sky"]).convert()
    bg = pygame.transform.scale(bg, (gs.width, gs.height))
    screen.blit(bg, (0, 0))

    #Draw all the created blocks to the screen
    #worldBlocks.draw(screen)
    
    #blits the player to the screen based on the location of the player
    #screen.blit(text, textRect)


    
    #screen.blit(player.image, (player.rect.x, player.rect.y))
    
    collisionblocks=camera.draw(screen,worldBlocks)   #draws all blocks in the viewable screen and returns all blocks within a small range to be used for collison in the next time step
    screen.blit(fpsText, (gs.blockSize*gs.noXBlocks-100, 5))
    inv.drawHotBar(screen)

    playerCraftingDistance = abs(player.getPlayerPos()[0] - gs.craftingTablePos[0]) + abs(player.getPlayerPos()[1] - gs.craftingTablePos[1]) 

    if(playerCraftingDistance > gs.blockSize * 6):
        gs.drawCrafting = False

    if(gs.drawCrafting):
        crafter.makeScreen()
        
    else:
        crafter.resetTable()
    

    #Finally update the  screen with all the above changes     
    pygame.display.update()


        

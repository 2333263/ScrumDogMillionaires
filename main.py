from matplotlib.pyplot import draw
import pygame
import pygame_gui
import gameSettings as gs
from levelGenerator import getBlocks
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerMovement as pm
import craftingMenu as cm
#Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()
deltaClock = pygame.time.Clock()


#Creating the pygame screen
screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

manager = pygame_gui.UIManager((gs.width, gs.height))

#Game runing variable
gameRunning = True

#Array to keep track of all the blocks in the world
worldBlocks = getBlocks(gs.levelName)

craftingItems = ["pickaxe", "wood", "sticks"]
cm.createCraftingList(craftingItems, manager)

#initilize a player object with attributes, position (x,y) and size (horizontal size, verical size is 2x horizontal)
player=pm.Player((100,gs.height/8), gs.blockSize)

#main game loop:
while gameRunning:
    clock.tick(60) #Sets the frame to update 60 times a second
    deltaTime = deltaClock.tick(60)/1000.0

    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            gameRunning = False

        manager.process_events(events)

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
                
            elif events.button == 3:
                bph.blockPlace(pygame.mouse.get_pos(), worldBlocks, player) #place the block
                
                #Maybe add the crafting button here
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

    manager.update(deltaTime)

    #runs the move on X which checks if the player is pressing an arrow key to move
    player.MoveOnX()
    #update the player position
    player.update(worldBlocks, clock.tick())


    #VERY TEMPORARY, here to make the placing easier when debugging itemIDs 
    #Create a font that displays the current block and count, also create a rectangle to draw the font to
    font = pygame.font.Font('freesansbold.ttf', 16)
    text = font.render('Block Selected: ' + gs.itemIDs[inv.selected] + ' : ' + str(inv.getSelected().getCount()), True, "white")
    textRect = text.get_rect()
    textRect.center = (4.5 * gs.blockSize, gs.blockSize)
    #add a frame rate counter to top right corner
    text2 = font.render("FPS: "+str(int(clock.get_fps())), 1, (0, 0, 0))

    #Create the sky 
    screen.fill(gs.colorNames["Sky"])
    
    #Draw all the created blocks to the screen
    for block in worldBlocks:
        screen.blit(block.Image, block.blockPosition)

    #blits the player to the screen based on the location of the player
    screen.blit(text, textRect)
    screen.blit(text2, (gs.width-100, 5))
    screen.blit(player.image, (player.rect.x, player.rect.y))


    if(gs.drawCrafting):
        pygame.draw.rect(screen, (105, 105, 105), pygame.Rect(gs.craftingPos[0] - 45, gs.craftingPos[1] - 130, 120, 100))
        manager.draw_ui(screen)
       
    
    pygame.display.update()

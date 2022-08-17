import pygame
import gameSettings as gs
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerHandler as ph
import Camera as cam
import CraftingMenu as cm
import menuHandler as mh
import time
from ChunkGenerator import generateChunk
from ChunkHandler import checkChunkUpdates
from soundHandler import playMusic
import Portal as po
from block import Block

#force update
# Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((gs.width, gs.height), vsync=1)
pygame.display.set_caption("2D Minecraft")

# Game running variable
gameRunning = True


color_light = (250, 250, 250)  # colour of button when hover over
color_dark = (64, 64, 64)  # colour of button-default

buttonFont = pygame.font.Font('Minecraft.ttf', 40)  # font for button
# load image for start screen
startPage = pygame.image.load("Textures/Screens/start.png")
startPage = pygame.transform.scale(
    startPage, (gs.width, gs.height))  # fit to page

# load image for pause screen
pausePage = pygame.image.load("Textures/Screens/finalPause.png")
pausePage = pygame.transform.scale(
    pausePage, (gs.width, gs.height))  # fit to page

# load image for information screen
infoPage = pygame.image.load("Textures/Screens/gameInfo.png")
infoPage = pygame.transform.scale(
    infoPage, (gs.width/1.5, gs.height/1.5))  # fit to page

# load image for end screen
endPage = pygame.image.load("Textures/Screens/endscreenNorestart.png")
endPage = pygame.transform.scale(endPage, (gs.width, gs.height))  # fit to page

#seed box font
base_font = pygame.font.Font(None, 32)
seedFont  = pygame.font.Font('freesansbold.ttf',32)
user_text = ''
#input rectangle
#rect for seed input
input_rect = pygame.Rect(80, 20, 100, 30)

text = base_font.render('SEED: ', True, (0,0,0))
textRect = text.get_rect()
textRect = (10,25)

text_surface = base_font.render("SEED:", False, (0,0,0))

color_active = pygame.Color(color_light)
color_passive = pygame.Color(color_dark)
color = color_passive
activeBox= False




inv.initGroup()
# Loading and playing a sound effect:
playMusic()


# main game loop:


def gameMenu():
    gameRunning = True
    # Array to keep track of all the blocks aaaaa in the world

    worldBlocks = pygame.sprite.Group()

    # list of blocks player can collide with, initially entire world but updated within first time step
    collisionblocks = worldBlocks
    gs.generatedChunks[-1] = generateChunk(-gs.CHUNK_SIZE[0], worldBlocks)
    gs.generatedChunks[0] = generateChunk(0, worldBlocks)
    gs.generatedChunks[1] = generateChunk(gs.CHUNK_SIZE[0], worldBlocks)

    # initilize a player object with attributes, position (x,y) and size (horizontal size, vertical size is 2x horizontal)
    # player = ph.Player((gs.width/2 - gs.blockSize * 4, gs.height/3), gs.blockSize)
    player = ph.Player((gs.width/2 - gs.blockSize * 4,
                      - gs.blockSize*2), gs.blockSize)
    camera = cam.Camera(player)
    checkChunkUpdates(player, worldBlocks)

    # Initilise breaking speed times
    startTime = 0
    startPos = 0

    # Initialise the crafting table screen
    crafter = cm.Crafting(screen)
 
    mouseDownCheck = False
    while gameRunning:
       
        clock.tick(60)  # Sets the frame to update 60 times a second

        for events in pygame.event.get():

            if events.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                quit()
            # Logic for player interaction
            # 1 -- left click
            # 2 -- middle click
            # 3 -- right click
            # 4 -- scroll up
            # 5 -- scroll down
            if (events.type == pygame.ACTIVEEVENT):
                if (events.gain == 0):
                    mh.mouseOffPause(clock)
            
            if events.type == pygame.MOUSEBUTTONDOWN:

                # Will add tool checks after each event.button check for effeciency, and other aspects (when we get there)
                if events.button == 1:

                    

                    if(inv.fullInv == False):
                        # Code for break speed:
                        mouseDownCheck = True;
                        startTime = time.time();
                        startPos = gs.getPos(pygame.mouse.get_pos() + camera.getOffsets())
                        # break the block


                    inv.onClick(pygame.mouse.get_pos())
                    crafter.onClick(pygame.mouse.get_pos())

                elif(not gs.drawCrafting):
                    if (events.button == 3 and inv.fullInv == False):
                        # Place a block

                        bph.blockPlace(pygame.mouse.get_pos(
                        ) + camera.getOffsets(), worldBlocks, player,False)  # place the block

                    # Scroll UP to select next item in hotbar
                    elif events.button == 4:
                        inv.selectNext()

                    # Scroll DOWN to select previous item in hotbar
                    elif events.button == 5:
                        inv.selectPrevious()

            # Code for break speed:

            elif events.type == pygame.MOUSEBUTTONUP:
               if events.button == 1:
                   mouseDownCheck = False;

            # if a key is pressed and that key is the up arrow, run the jump method in the player class
            elif(events.type == pygame.KEYDOWN):
                if((events.key == pygame.K_UP or events.key == pygame.K_SPACE) and not gs.drawCrafting):
                    player.jump()
                elif(events.key == pygame.K_ESCAPE):
                    gs.drawCrafting = False
                    if(inv.fullInv == True):
                        inv.fullInv = False  # hides full inventory
                        inv.clicked = -1
                elif(events.key == pygame.K_p):
                    mh.pauseMenu(screen, clock, pausePage)
                elif(events.key == pygame.K_e):
                    if(inv.fullInv == False):
                        inv.fullInv = True  # displays full inventory
                    else:
                        inv.fullInv = False
                        inv.clicked = -1
        
        if(not gs.drawCrafting):
            # runs the move on X which checks if the player is pressing an arrow key to move
            fakeKeys = {}
            player.MoveOnX(fakeKeys)
            # update the player position
            player.update(clock.tick(),  collisionblocks)

        # Font to draw the FPS
        font = pygame.font.Font('Minecraft.ttf', 16)
        fpsText = font.render(
            "FPS: "+str(int(clock.get_fps())), 1, (255, 255, 255))
        seedText = font.render("Seed: " + str(gs.seed), 1, (255, 255, 255))

        # Create the sky background
        bg = pygame.image.load(gs.textureNames["Sky"]).convert()
        bg = pygame.transform.scale(bg, (gs.width, gs.height))
        screen.blit(bg, (0, 0))

        # Draws all blocks in the viewable screen and returns all blocks within a small range to be used for collison in the next time step
        collisionblocks = camera.draw(screen, worldBlocks)
        screen.blit(fpsText, (1180, 5))
        screen.blit(seedText, (1180, 50))
        crafter.initGroup()
        if(gs.drawCrafting):
            crafter.drawCraft()
            inv.fullInv=True
        inv.drawHotBar(screen)
        
        
        blockFrameImgName = "Block_Frame_Red"

        # Breaking speed
        breakTime = 1
        if (mouseDownCheck):
            if (startPos != gs.getPos(pygame.mouse.get_pos() + camera.getOffsets())):
                # Restart timer if player moves blocks
                startPos = gs.getPos(pygame.mouse.get_pos() + camera.getOffsets())
                startTime = time.time()
                # print('moved cursor')
            if (time.time() - startTime >= breakTime):
                bph.blockBreak(pygame.mouse.get_pos() + camera.getOffsets(), worldBlocks, player,False)
            # Break block if timer is longer than required
        # Draws a box around the selected block

        block = bph.getBlockFromPos(
            gs.getPos(pygame.mouse.get_pos()+camera.getOffsets()), worldBlocks)
        if(block.itemID != -1):
            if block.itemID in gs.clickableBlocks:
                blockFrameImgName = "Block_Frame"
            if bph.checkBreakable(block, inv.invArray[inv.selected]):
                # Different cursors for different levels of breakage
                if (mouseDownCheck):
                    # Steps for breaking speed
                    if (time.time() - startTime <= breakTime * 1 / 4):
                        blockFrameImgName = "Block_Frame_Green_1_4"
                    elif (time.time() - startTime <= breakTime * 2 / 4):
                        blockFrameImgName = "Block_Frame_Green_2_4"
                    elif (time.time() - startTime <= breakTime * 3 / 4):
                        blockFrameImgName = "Block_Frame_Green_3_4"
                    elif (time.time() - startTime <= breakTime * 4 / 4):
                        blockFrameImgName = "Block_Frame_Green_4_4"
                    else:
                        blockFrameImgName = "Block_Frame_Green"

                else:
                    blockFrameImgName = "Block_Frame_Green"

        else:
            blockFrameImgName = "Block_Frame"
        blockFrameImg = pygame.image.load(gs.textureNames[blockFrameImgName]).convert_alpha()
        blockFrame = pygame.transform.scale(
            blockFrameImg, (gs.blockSize, gs.blockSize))
        mousePos = pygame.mouse.get_pos()[0] + camera.getOffsets()[0] % gs.blockSize, \
            pygame.mouse.get_pos()[1] + camera.getOffsets()[1] % gs.blockSize

        # Calculate final position
        blockPos = gs.getPos(mousePos)[0] - camera.getOffsets()[0] % gs.blockSize, \
            gs.getPos(mousePos)[1] - camera.getOffsets()[1] % gs.blockSize
       
        # Draw cursor only if block is within interactable range (place/break) and won't collide with player
        tempNullBlock = Block(gs.blockSize, gs.getPos(pygame.mouse.get_pos()+camera.getOffsets()),
                              1, gs.textureNames[gs.itemIDs[1]], hardness=1)  # replace with nulltexture when added
        if (not inv.fullInv):
            if gs.distance(player, pygame.mouse.get_pos()+camera.getOffsets()) <= gs.playerRange * gs.blockSize and (not player.willcollide(tempNullBlock) or not blockFrameImgName == "Block_Frame"):
                screen.blit(blockFrame, blockPos)

        if(gs.endGamePos[0] != -1 and gs.drawPortal):
            blockTemp = Block(gs.blockSize, gs.endGamePos, 26,
                              gs.textureNames["Portal Block"], 999)
            worldBlocks.add(blockTemp)
            mh.endMenu(screen, clock, endPage)

      

        checkChunkUpdates(player, worldBlocks)

        print(player.getPlayerPos())

        # Finally update the  screen with all the above changes
        pygame.display.update()


while gameRunning:
    # start screen
    
    clock.tick(60)  # Sets the frame to update 60 times a second
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            pygame.mixer.music.stop()  # stops the music player
            gameRunning = False
    
        if events.type == pygame.MOUSEBUTTONDOWN:
            # if the mouse is clicked on the button,the game begins
            if gs.width/2-110 <= mouse[0] <= gs.width/2+190 and gs.height/2+50 <= mouse[1] <= gs.height/2+130:
                gs.setSeed(user_text) #sets seed in gameSettings
                gameMenu()  # call main game loop
            elif gs.width/2-110 <= mouse[0] <= gs.width/2+190 and gs.height/2+200 <= mouse[1] <= gs.height/2+280:
                pygame.quit()
                quit()
            elif gs.width-110 <= mouse[0] <= gs.width-70 and 10 <= mouse[1] <= 50:
                mh.infoMenu(screen, clock, infoPage)

            #if mouse clicks on seed box
            if input_rect.collidepoint(events.pos):
                activeBox= True
            else:
                activeBox= False
        if events.type == pygame.KEYDOWN and activeBox==True:
            #check for backspace
            if events.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
                
            elif len(user_text)<7:#add seed char to input string
                user_text += events.unicode
    #sets colour for seed text box based on if it has been clicked on
    if activeBox: 
        color =  color_active
    else:
        color = color_passive
    screen.blit(startPage, (0, 0))  # put the start page on the screen
    mouse = pygame.mouse.get_pos()  # get mouse positions

    if gs.width/2-130 <= mouse[0] <= gs.width/2+170 and gs.height/2+50 <= mouse[1] <= gs.height/2+130:
        # if we are hovering over the start button, draw it with the lighter colour
        pygame.draw.rect(screen, color_light, [
                         gs.width/2-130, gs.height/2+50, 300, 80])
        # rendering a text written in this font for the start button
        startButtonText = buttonFont.render('BEGIN GAME', True, (0, 0, 0))

    else:
        # if we are not hovering over the start button, draw it with the darker colour
        pygame.draw.rect(screen, color_dark, [
                         gs.width/2-130, gs.height/2+50, 300, 80])
        # rendering a text written in this font for the start button
        startButtonText = buttonFont.render(
            'BEGIN GAME', True, (255, 255, 255))

    if gs.width/2-130 <= mouse[0] <= gs.width/2+170 and gs.height/2+200 <= mouse[1] <= gs.height/2+280:
        # if we are hovering over the exit button, draw it with the lighter colour
        pygame.draw.rect(screen, color_light, [
                         gs.width/2-130, gs.height/2+200, 300, 80])
        # rendering a text written in this font for the exit button
        exitButtonText = buttonFont.render('EXIT GAME', True, (0, 0, 0))

    else:
        # if we are not hovering over the exit button, draw it with the darker colour
        pygame.draw.rect(screen, color_dark, [
                         gs.width/2-130, gs.height/2+200, 300, 80])
        # rendering a text written in this font for the exit button
        exitButtonText = buttonFont.render('EXIT GAME', True, (255, 255, 255))

    if gs.width-110 <= mouse[0] <= gs.width-70 and 10 <= mouse[1] <= 50:
        # if we are hovering over the information button ?, draw it with the lighter colour
        pygame.draw.rect(screen, color_light, [gs.width-110, 10, 40, 40])
        # rendering a text written in this font for the information button
        informationButonText = buttonFont.render('?', True, (0, 0, 0))

    else:
        # if we are not hovering over the information button, draw it with the darker colour
        pygame.draw.rect(screen, color_dark, [gs.width-110, 10, 40, 40])
        # rendering a text written in this font for the information button
        informationButonText = buttonFont.render('?', True, (255, 255, 255))
    

    #render seed box
    pygame.draw.rect(screen, color, input_rect)
    text_surface = base_font.render(user_text, False, (0,0,0))
    screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    screen.blit(text, textRect)

    # display text on information button
    screen.blit(informationButonText, (gs.width-100, 17))
    # display text on exit button
    screen.blit(exitButtonText, (gs.width/2-90, gs.height/2+225))
    # display text on start button
    screen.blit(startButtonText, (gs.width/2-107, gs.height/2+75))

    

    pygame.display.flip()

import pygame
import gameSettings as gs
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerHandler as ph
import Camera as cam
import CraftingMenu as cm
import menuHandler as  mh
from ChunkGenerator import generateChunk
#Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((gs.width, gs.height))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
gameRunning = True

color_light = (250,250,250) #colour of button when hover over
color_dark = (64,64,64) #colour of button- default

buttonFont = pygame.font.Font('Minecraft.ttf', 40) #font for button
startPage = pygame.image.load("Textures/Screens/start.png") #load image for start screen
startPage = pygame.transform.scale(startPage, (gs.width, gs.height)) #fit to page

pausePage = pygame.image.load("Textures/Screens/finalPause.png") #load image for pause screen
pausePage = pygame.transform.scale(pausePage, (gs.width, gs.height)) #fit to page

infoPage = pygame.image.load("Textures/Screens/gameInfo.png") #load image for information screen
infoPage = pygame.transform.scale(infoPage, (gs.width/1.5, gs.height/1.5)) #fit to page

inv.initGroup()
     
#main game loop:
def gameMenu():
    gameRunning=True
    #Array to keep track of all the blocks in the world
 
    worldBlocks = pygame.sprite.Group()

    collisionblocks=worldBlocks #list of blocks player can collide with, initially entire world but updated within first time step
    
    

    for i in range(-5, 5, 1):
        gs.generatedChunks[i] = generateChunk(64 * i, worldBlocks)

    #initilize a player object with attributes, position (x,y) and size (horizontal size, verical size is 2x horizontal)
    # player = ph.Player((gs.width/2 - gs.blockSize * 4, gs.height/3), gs.blockSize)
    player = ph.Player((gs.width/2 - gs.blockSize * 4, gs.blockSize*6), gs.blockSize)
    camera=cam.Camera(player)

    #Initilise breaking speed times
    startTime = 0
    startPos = 0

    #Initialise the crafting table screen 
    crafter = cm.Crafting(screen)
    
    while gameRunning:
        clock.tick(60) #Sets the frame to update 60 times a second

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
            if events.type == pygame.MOUSEBUTTONDOWN:
                #Will add tool checks after each event.button check for effeciency, and other aspects (when we get there)
                if events.button == 1:
                    if(gs.drawCrafting):
                        crafter.checkClick(pygame.mouse.get_pos()) 
                        crafter.makeItem(pygame.mouse.get_pos())
                        
                    elif(inv.fullInv==False):
                        #Code for break speed:
                        #startTime = pygame.time.get_ticks() / 1000
                        #startPos = gs.getPos(pygame.mouse.get_pos())
                        bph.blockBreak(pygame.mouse.get_pos()+camera.getOffsets(), worldBlocks, player) #break the block

                    inv.onClick(pygame.mouse.get_pos())

                elif(not gs.drawCrafting):
                    if (events.button == 3 and inv.fullInv==False):
                        #Place a block
                        bph.blockPlace(pygame.mouse.get_pos()+camera.getOffsets(), worldBlocks, player) #place the block
                        
                    #Scroll UP to select next item in hotbar
                    elif events.button == 4:
                        inv.selectNext()

                    #Scroll DOWN to select previous item in hotbar
                    elif events.button == 5:
                        inv.selectPrevious()

            #Code for break speed:
            
            #elif events.type == pygame.MOUSEBUTTONUP:
            #    if events.button == 1:
            #        endTime = pygame.time.get_ticks()/1000
            #        endPos = gs.getPos(pygame.mouse.get_pos())
            #        # Speed is roughly ~0.5 seconds
            #        timeToBreak = 0.5
            #        if (endTime-startTime >=timeToBreak and startPos==endPos):
            #            bph.blockBreak(pygame.mouse.get_pos() + camera.getOffsets(), worldBlocks, player)  # break the block
            

            #if a key is pressed and that key is the up arrow, run the jump method in the player class
            elif(events.type==pygame.KEYDOWN ):
                if((events.key==pygame.K_UP or events.key==pygame.K_SPACE) and not gs.drawCrafting):
                    player.jump()
                elif(events.key == pygame.K_ESCAPE):
                    gs.drawCrafting = False
                    if(inv.fullInv==True):
                        inv.fullInv=False      #hides full inventory
                        inv.clicked=-1
                elif(events.key==pygame.K_p):
                    mh.pauseMenu(screen,clock,pausePage)
                elif(events.key==pygame.K_e):
                    if(inv.fullInv==False):
                        inv.fullInv=True        #displays full inventory
                    else:
                        inv.fullInv=False
                        inv.clicked=-1

        if(not gs.drawCrafting):
            #runs the move on X which checks if the player is pressing an arrow key to move
            fakeKeys={}
            player.MoveOnX(fakeKeys)
            #update the player position
            player.update(clock.tick(),  collisionblocks)


        #Font to draw the FPS
        font = pygame.font.Font('Minecraft.ttf', 16)
        fpsText = font.render("FPS: "+str(int(clock.get_fps())), 1, (255, 255, 255))
        seedText = font.render("Seed: " +str(gs.seed), 1, (255, 255, 255))

        #Create the sky background
        bg = pygame.image.load(gs.textureNames["Sky"]).convert()
        bg = pygame.transform.scale(bg, (gs.width, gs.height))
        screen.blit(bg, (0, 0))

        #Draws all blocks in the viewable screen and returns all blocks within a small range to be used for collison in the next time step
        collisionblocks=camera.draw(screen,worldBlocks)   
        screen.blit(fpsText, (1180, 5))
        screen.blit(seedText, (1180, 50))
        inv.drawHotBar(screen)

        #Draws a box around the selected block
        blockFrameImg = pygame.image.load(gs.textureNames["Block_Frame"])
        blockFrame = pygame.transform.scale(blockFrameImg, (gs.blockSize, gs.blockSize))
        mousePos = pygame.mouse.get_pos()[0] + camera.getOffsets()[0] % gs.blockSize, \
                   pygame.mouse.get_pos()[1] + camera.getOffsets()[1] % gs.blockSize

        #Calculate final position
        blockPos = gs.getPos(mousePos)[0] - camera.getOffsets()[0] % gs.blockSize, \
                   gs.getPos(mousePos)[1] - camera.getOffsets()[1] % gs.blockSize
        #Draw cursor only if block is within interactable range (place/break)
        if gs.distance(player, pygame.mouse.get_pos()+camera.getOffsets()) <= gs.playerRange * gs.blockSize and gs.distance(player, pygame.mouse.get_pos()+camera.getOffsets())>0.8*gs.blockSize and  gs.distance(player, pygame.mouse.get_pos()+camera.getOffsets()-[0,gs.blockSize])>0.8*gs.blockSize:
            screen.blit(blockFrame, blockPos)

        if(gs.drawCrafting):
            crafter.makeScreen()  
        else:
            crafter.resetTable()
        
        print(player.rect.x//gs.blockSize)

        #Finally update the  screen with all the above changes     
        pygame.display.update()

    
while gameRunning:
    #start screen
    clock.tick(60) #Sets the frame to update 60 times a second
    for events in pygame.event.get():    
        if events.type == pygame.QUIT:
            gameRunning = False
        if events.type == pygame.MOUSEBUTTONDOWN: 
              
            #if the mouse is clicked on the button,the game begins
            if gs.width/2-110 <= mouse[0] <= gs.width/2+190 and gs.height/2+50 <= mouse[1] <= gs.height/2+130: 
                gameMenu() #call main game loop
            elif gs.width/2-110 <= mouse[0] <= gs.width/2+190 and gs.height/2+200 <= mouse[1] <= gs.height/2+280:
                pygame.quit()
                quit()
            elif gs.width-110 <= mouse[0] <= gs.width-70 and 10 <= mouse[1] <= 50:
                mh.infoMenu(screen,clock,infoPage)
        

    screen.blit(startPage,(0,0) ) #put the start page on the screen
    mouse = pygame.mouse.get_pos() #get mouse positions
    


    if gs.width/2-110 <= mouse[0] <= gs.width/2+190 and gs.height/2+50 <= mouse[1] <= gs.height/2+130: 
        #if we are hovering over the start button, draw it with the lighter colour
        pygame.draw.rect(screen,color_light,[gs.width/2-110,gs.height/2+50,300,80]) 
        startButtonText = buttonFont.render('BEGIN GAME' , True , (0,0,0) )  #rendering a text written in this font for the start button
          
    else: 
        #if we are not hovering over the start button, draw it with the darker colour
        pygame.draw.rect(screen,color_dark,[gs.width/2-110,gs.height/2+50,300,80]) 
        startButtonText = buttonFont.render('BEGIN GAME' , True , (255,255,255) )  #rendering a text written in this font for the start button
        
    if gs.width/2-110 <= mouse[0] <= gs.width/2+190 and gs.height/2+200 <= mouse[1] <= gs.height/2+280: 
        #if we are hovering over the exit button, draw it with the lighter colour
        pygame.draw.rect(screen,color_light,[gs.width/2-110,gs.height/2+200,300,80]) 
        exitButtonText = buttonFont.render('EXIT GAME' , True , (0,0,0) )  #rendering a text written in this font for the exit button
          
    else: 
        #if we are not hovering over the exit button, draw it with the darker colour
        pygame.draw.rect(screen,color_dark,[gs.width/2-110,gs.height/2+200,300,80]) 
        exitButtonText = buttonFont.render('EXIT GAME' , True , (255,255,255) )  #rendering a text written in this font for the exit button
        
    if gs.width-110 <= mouse[0] <= gs.width-70 and 10 <= mouse[1] <= 50: 
        #if we are hovering over the information button, draw it with the lighter colour
        pygame.draw.rect(screen,color_light,[gs.width-110,10,40,40]) 
        informationButonText= buttonFont.render('?' , True , (0,0,0) )  #rendering a text written in this font for the information button
          
    else: 
        #if we are not hovering over the information button, draw it with the darker colour
        pygame.draw.rect(screen,color_dark,[gs.width-110,10,40,40])
        informationButonText= buttonFont.render('?' , True , (255,255,255) )  #rendering a text written in this font for the information button
    
    
    
    screen.blit(informationButonText , (gs.width-100,17)) # display text on information button
    screen.blit(exitButtonText , (gs.width/2-75,gs.height/2+225)) # display text on exit button 
    screen.blit(startButtonText , (gs.width/2-85,gs.height/2+75)) # display text on start button 
      
    pygame.display.update()



    

    


        

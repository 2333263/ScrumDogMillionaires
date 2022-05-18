import pygame
import gameSettings as gs
from levelGenerator import getBlocks
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerHandler as ph
import Camera as cam#Why would we call this cam like why CAM2007A
import CraftingMenu as cm

#Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()

#Creating the pygame screen
width=gs.blockSize*gs.noXBlocks
height=gs.blockSize*gs.noYBlocks
screen = pygame.display.set_mode((gs.blockSize*gs.noXBlocks, gs.blockSize*gs.noYBlocks))
pygame.display.set_caption("2D Minecraft")

#Game runing variable
gameRunning = True

color_light = (250,250,250) #colour of button when hover over
color_dark = (255, 165, 0) #colour of button- default
buttonFont = pygame.font.SysFont('Corbel',50) #font for button
startButtonText = buttonFont.render('BEGIN GAME' , True , (0,0,0) )  #rendering a text written in this font for the start button
exitButtonText = buttonFont.render('EXIT GAME' , True , (0,0,0) )  #rendering a text written in this font for the exit button
startPage = pygame.image.load("Textures/Screens/startscreen.PNG") #load image for start screen
startPage = pygame.transform.scale(startPage, (gs.width, gs.height)) #fit to page
pausePage = pygame.image.load("Textures/Screens/pause.PNG") #load image for pause screen
pausePage = pygame.transform.scale(pausePage, (gs.width, gs.height)) #fit to page

#pause menu - pops up when user clicks key "p"
def pauseMenu():
    paused= True #the user has paused the game
    while paused:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_c: #if the user clicks c, resume game
                    paused=False
                elif event.key==pygame.K_q: #if the user clicks q, quit game
                    pygame.quit()
                    quit()
        screen.blit(pausePage,(0,0) ) #display the pause screen
        pygame.display.update()
        clock.tick(60)
        
#main game loop:
def gameMenu():
    gameRunning=True
    #Array to keep track of all the blocks in the world
    worldBlocks = getBlocks(gs.levelName)
    collisionblocks=worldBlocks #list of blocks player can collide with, initially entire world but updated within first time step

    #initilize a player object with attributes, position (x,y) and size (horizontal size, verical size is 2x horizontal)
    player = ph.Player((gs.width/2 - gs.blockSize * 4, gs.height/3), gs.blockSize)
    camera=cam.Camera(player)

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
                    else:
                        bph.blockBreak(pygame.mouse.get_pos()+camera.getOffsets(), worldBlocks, player) #break the block
                    
                elif(not gs.drawCrafting):
                    if events.button == 3:
                        #Place a block
                        bph.blockPlace(pygame.mouse.get_pos()+camera.getOffsets(), worldBlocks, player) #place the block
                        
                    #Scroll UP to select next item in hotbar
                    elif events.button == 4:
                        inv.selectNext()

                    #Scroll DOWN to select previous item in hotbar
                    elif events.button == 5:
                        inv.selectPrevious()

            #if a key is pressed and that key is the up arrow, run the jump method in the player class
            elif(events.type==pygame.KEYDOWN ):
                if((events.key==pygame.K_UP or events.key==pygame.K_SPACE) and not gs.drawCrafting):
                    player.jump()
                elif(events.key == pygame.K_ESCAPE):
                    gs.drawCrafting = False
                elif(events.key==pygame.K_p):
                    pauseMenu()

        if(not gs.drawCrafting):
            #runs the move on X which checks if the player is pressing an arrow key to move
            fakeKeys={}
            player.MoveOnX(fakeKeys)
            #update the player position
            player.update(clock.tick(),  collisionblocks)

        
        #Font to draw the FPS
        font = pygame.font.Font('Minecraft.ttf', 16)
        fpsText = font.render("FPS: "+str(int(clock.get_fps())), 1, (0, 0, 0))

        #Create the sky     
        bg = pygame.image.load(gs.textureNames["Sky"]).convert()
        bg = pygame.transform.scale(bg, (gs.width, gs.height))
        screen.blit(bg, (0, 0))

        #Draws all blocks in the viewable screen and returns all blocks within a small range to be used for collison in the next time step
        collisionblocks=camera.draw(screen,worldBlocks)   
        screen.blit(fpsText, (gs.blockSize*gs.noXBlocks-100, 5))
        inv.drawHotBar(screen)

        if(gs.drawCrafting):
            crafter.makeScreen()  
        else:
            crafter.resetTable()
        

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
            if width/2-110 <= mouse[0] <= width/2+190 and height/2+50 <= mouse[1] <= height/2+130: 
                gameMenu() #call main game loop
            elif width/2-110 <= mouse[0] <= width/2+190 and height/2+200 <= mouse[1] <= height/2+280:
                pygame.quit()
                quit()
        

    screen.blit(startPage,(0,0) ) #put the start page on the screen
    mouse = pygame.mouse.get_pos() #get mouse positions
    if width/2-110 <= mouse[0] <= width/2+190 and height/2+50 <= mouse[1] <= height/2+130: 
        #if we are hovering over the start button, draw it with the lighter colour
        pygame.draw.rect(screen,color_light,[width/2-110,height/2+50,300,80]) 
          
    else: 
        #if we are not hovering over the start button, draw it with the darker colour
        pygame.draw.rect(screen,color_dark,[width/2-110,height/2+50,300,80]) 
        
    if width/2-110 <= mouse[0] <= width/2+190 and height/2+200 <= mouse[1] <= height/2+280: 
        #if we are hovering over the exit button, draw it with the lighter colour
        pygame.draw.rect(screen,color_light,[width/2-110,height/2+200,300,80]) 
          
    else: 
        #if we are not hovering over the exit button, draw it with the darker colour
        pygame.draw.rect(screen,color_dark,[width/2-110,height/2+200,300,80]) 
        
    
    screen.blit(exitButtonText , (width/2-75,height/2+220)) # display text on exit button 
    screen.blit(startButtonText , (width/2-100,height/2+70)) # display text on start button 
      
    pygame.display.update()



    

    


        

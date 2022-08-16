import pygame
import gameSettings as gs
import breakPlaceHandler as bph
import inventoryHandler as inv
import playerHandler as ph
import Camera as cam
import CraftingMenu as cm
import time
from ChunkGenerator import generateChunk
from ChunkHandler import checkChunkUpdates
from itemHandler import populateDictionaries
import random

# Populate item dictionaries
populateDictionaries()

# force update
# Initialising PyGame & creating a clock in order to limit frame drawing
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((gs.width, gs.height), vsync=1)
pygame.display.set_caption("2D Minecraft")

inv.initGroup()

currentAction = gs.actions["NONE"]#-1 is no simulated key press

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
        currentAction = random.choice([-1, 0, 1, 2, 3, 4])
        if(currentAction == 0):
            print("JUMP")
        clock.tick(15)  # Sets the frame to update 60 times a second

       
        for events in pygame.event.get():
     
            if events.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                quit()

            # if events.type == pygame.MOUSEBUTTONDOWN:
            #     # Will add tool checks after each event.button check for effeciency, and other aspects (when we get there)
            #     if events.button == 1:
            #         if(inv.fullInv == False):
            #             # Code for break speed:
            #             mouseDownCheck = True
            #             startTime = time.time()
            #             startPos = gs.getPos(pygame.mouse.get_pos() + camera.getOffsets())
            #             # break the block

            #         inv.onClick(pygame.mouse.get_pos())
            #         crafter.onClick(pygame.mouse.get_pos())

            #     elif(not gs.drawCrafting):
            #         if (events.button == 3 and inv.fullInv == False):
            #             # Place a block

            #             bph.blockPlace(pygame.mouse.get_pos() +
            #                            camera.getOffsets(), worldBlocks, player, False)  # place the block

            #         # Scroll UP to select next item in hotbar
            #         elif events.button == 4:
            #             inv.selectNext()

            #         # Scroll DOWN to select previous item in hotbar
            #         elif events.button == 5:
            #             inv.selectPrevious()

            # Code for break speed:

            # elif events.type == pygame.MOUSEBUTTONUP:
            #     if events.button == 1:
            #         mouseDownCheck = False

            # if a key is pressed and that key is the up arrow, run the jump method in the player class
            # elif(events.type == pygame.KEYDOWN ) :
            #     if((events.key == pygame.K_UP or events.key == pygame.K_SPACE) and not gs.drawCrafting):
            #         player.jump()
            #     elif(events.key == pygame.K_ESCAPE):
            #         gs.drawCrafting = False
            #         if(inv.fullInv == True):
            #             inv.fullInv = False  # hides full inventory
            #             inv.clicked = -1

            #     elif(events.key == pygame.K_e):
            #         if(inv.fullInv == False):
            #             inv.fullInv = True  # displays full inventory
            #         else:
            #             inv.fullInv = False
            #             inv.clicked = -1


            if(currentAction == gs.actions["JUMP"] ):
                player.jump()

            elif(currentAction == gs.actions["EXIT"]):
                gs.drawCrafting = False
                if(inv.fullInv == True):
                    inv.fullInv = False  # hides full inventory
                    inv.clicked = -1
                
            elif(currentAction == gs.actions["INVENTORY"]):
                if(inv.fullInv == False):
                    inv.fullInv = True  # displays full inventory
                else:
                    inv.fullInv = False
                    inv.clicked = -1

        bg = pygame.Rect(0, 0, gs.width, gs.height)
        pygame.draw.rect(screen, (0, 0, 0), bg)
        
        if(not gs.drawCrafting):
            # runs the move on X which checks if the player is pressing an arrow key to move
            fakeKeys = {}
            player.MoveOnX(fakeKeys, currentAction)
            # update the player position
            player.update(clock.tick(),  collisionblocks)

        # Draws all blocks in the viewable screen and returns all blocks within a small range to be used for collison in the next time step
        collisionblocks = camera.draw(screen, worldBlocks)
        crafter.initGroup()
        if(gs.drawCrafting):
            crafter.drawCraft()
            inv.fullInv = True
        inv.drawHotBar(screen)

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
     
        block = bph.getBlockFromPos(gs.getPos(pygame.mouse.get_pos()+camera.getOffsets()), worldBlocks)

        # Breaking speed
        breakTime = 1
        if (mouseDownCheck):
            if (startPos != gs.getPos(pygame.mouse.get_pos() + camera.getOffsets())):
                # Restart timer if player moves blocks
                startPos = gs.getPos(
                    pygame.mouse.get_pos() + camera.getOffsets())
                startTime = time.time()
                # print('moved cursor')
            if (time.time() - startTime >= breakTime):
                bph.blockBreak(pygame.mouse.get_pos() +
                               camera.getOffsets(), worldBlocks, player, False)

        checkChunkUpdates(player, worldBlocks)

        # Finally update the  screen with all the above changes
        pygame.display.update()
        pygame.display.flip()

        

gameMenu()

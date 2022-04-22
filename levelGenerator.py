import gameSettings as gs
from block import Block
import pygame

def getBlocks(levelName):
    gs.levelName = levelName
    worldGroup = pygame.sprite.Group()

    #Loop over every character
    for i in range(len(gs.levelArray)):
        for j in range(len(gs.levelArray[i])):
            currHeight = i * gs.blockSize
            currWidth = j * gs.blockSize

            #if its an air block or an extra line skip it 
            if(gs.levelArray[i][j] == ' ' or gs.levelArray[i][j] == '\n'):
                continue
        
            #Create a block using the current number in the level
            currItemID = int(gs.converterIDs[gs.levelArray[i][j]])
            if(gs.itemIDs.__contains__(currItemID)):
                if(currItemID == 5): #Deal with crafting table
                    b = Block(gs.blockSize, (currWidth, currHeight), currItemID, gs.textureNames[gs.itemIDs[currItemID]])
                    gs.craftingTablePos[0] = currWidth
                    gs.craftingTablePos[1] = currHeight
                else: #Deal with all other blocks in the world
                    b = Block(gs.blockSize, (currWidth, currHeight), currItemID, gs.textureNames[gs.itemIDs[currItemID]])
                worldGroup.add(b)
         
    return worldGroup
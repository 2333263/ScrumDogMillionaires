import gameSettings as gs
from block import Block

def getBlocks(levelName):
    blockArray = []
    gs.levelName = levelName
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
                if(currItemID == 3):
                    #Do cloud stuff
                    b = Block(gs.blockSize * 6, (currWidth, currHeight), currItemID, gs.textureNames[gs.itemIDs[currItemID]])
                else:
                    b = Block(gs.blockSize, (currWidth, currHeight), currItemID, gs.textureNames[gs.itemIDs[currItemID]])
                blockArray.append(b)
            

    return blockArray
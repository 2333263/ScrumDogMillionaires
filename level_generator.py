import game_settings as gs
from block import Block

def getBlocks(level_name):
    block_array = []
    gs.level_name = level_name
    #Loop over every character
    for i in range(len(gs.level_array)):
        for j in range(len(gs.level_array[i])):
            curr_height = i * gs.block_size
            curr_width = j * gs.block_size
            #if its an air block or an extra line skip it 
            if(gs.level_array[i][j] == ' ' or gs.level_array[i][j] == '\n'):
                continue
                
            #Create a block using the current number in the level
            currItemID = int(gs.level_array[i][j])
            if(gs.itemIDs.__contains__(currItemID)):
                b = Block(gs.block_size, (curr_width, curr_height),  currItemID, gs.textureNames[gs.itemIDs[currItemID]]) 
                block_array.append(b)
            

    return block_array
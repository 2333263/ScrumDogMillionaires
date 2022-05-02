import gameSettings as gs
import block
import inventoryHandler
import math
from block import Block
import inventoryHandler as inv


def distance(player, python_pos):
    playerPos = getPos(player.getPlayerPos())
    blockPos = getPos(python_pos)
    return math.sqrt(pow((playerPos[0] - blockPos[0]), 2) + (pow((playerPos[1] - blockPos[1]), 2)))

def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = gs.blockSize*math.floor(pos[0]/gs.blockSize),gs.blockSize*math.floor(pos[1]/gs.blockSize)
    return pos

def checkBreakable(block, inHand):
    blockHardness = block.getHardness()
    itemHardness = inHand.getHardness()
    if(itemHardness>=blockHardness):
        return True
    else:
        return False

def notEmpty(hotbarSelected):
    if hotbarSelected.isEmpty():
        return False
    else:
        return True

def blockBreak(python_pos, world_block, player): #Block breaking logic, and inventory handler passover
    if distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = getPos(python_pos)
        for block in world_block:
            if block.blockPosition == pos and block.itemID not in gs.immovableBlocks and len(inv.hotbarArr) > 0:
                if checkBreakable(block,inv.hotbarArr[inv.selected]):
                    #Remove block from world
                    world_block.remove(block)
                    #Add block to inventory
                    inv.addBlock(block)
            elif block.blockPosition == pos and block.itemID not in gs.immovableBlocks: 
                # payer is not holding a tool
                if block.getHardness()<=0:
                    #Remove block from world
                    world_block.remove(block)
                    #Add block to inventory
                    inv.addBlock(block)


def blockPlace(python_pos, world_block, player): #Block placing logic, and inventory handler requesting
    if distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = getPos(python_pos)
        found = False
        for block in world_block:
            if block.blockPosition == pos:
                if(block.itemID in gs.clickableBlocks):
                    if(gs.drawCrafting):
                        gs.drawCrafting = False
                    else:
                        gs.drawCrafting = True
                found = True
        if found == False:
            #Only allow placing if player has more blocks
            if (len(inv.hotbarArr)!=0 and inv.getSelected().amount >0):
                #Decrease inventory item
                

                #Add block to world
                if(gs.textureNames.__contains__(gs.itemIDs[inv.hotbarArr[inv.selected].getItemId()])):
                    currTexture = gs.textureNames[gs.itemIDs[inv.hotbarArr[inv.selected].getItemId()]]
                    if inv.hotbarArr[inv.selected].isPlaceable:
                        tempBlock = Block(gs.blockSize, pos,  inv.hotbarArr[inv.selected].getItemId(), currTexture, hardness = gs.blockHardness[inv.hotbarArr[inv.selected].getItemId()])
                        world_block.add(tempBlock)
                        inv.decrease()

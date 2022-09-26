import gameSettings as gs
from block import Block
import inventoryHandler as inv
from soundHandler import playBreakSoundforID
import itemHandler as ih

immovableBlocks = ih.immovableBlocks
clickableBlock = ih.clickableBlocks
textureNames = ih.fetchTextureNames()
itemIDs = ih.fetchItemIDs()
breakTimes = ih.fetchBreakTime()
blockHardness = ih.fetchBlockHardness()
def checkBreakable(block, inHand):
    # a block can only be broken if the current tool is harder than the block's hardness
    blockHardness = block.getHardness()
    itemHardness = inHand.getItemHardness()
    if(itemHardness >= blockHardness):
        return True
    else:
        return False

''' Deprecated??
def notEmpty(hotbarSelected):
    if hotbarSelected.isEmpty():
        return False
    else:
        return True
'''

# Block breaking logic, and inventory handler passover
def blockBreak(python_pos, world_block, player,test, sound = False):
    if gs.distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = gs.getPos(python_pos)
        block = getBlockFromPos(pos, world_block)
        # find correct block to break. Check if block is breakable. i.e. not bed rock/ crafting table
        if(block.itemID != -1):
            if block.itemID not in ih.immovableBlocks and len(inv.invArray) > 0:
                if checkBreakable(block, inv.invArray[inv.selected]):
                    # Remove block from world
                    world_block.remove(block)
                    gs.generatedChunks[gs.visibleChunks[1]].remove(block)
                    # Add block to inventory
                    inv.addBlock(block)
                     #call sound effect
                    if(test==False and sound):
                        playBreakSoundforID(block.itemID)
            elif block.itemID not in ih.immovableBlocks:
                # payer is not holding a tool
                if block.getHardness() <= 0:
                    # Remove block from world
                    world_block.remove(block)
                    gs.generatedChunks[gs.visibleChunks[1]].remove(block)
                    # Add block to inventory
                    inv.addBlock(block)


# Block placing logic, and inventory handler requesting
def blockPlace(python_pos, world_block, player,test, sound = False):
    if gs.distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = gs.getPos(python_pos)
        block = getBlockFromPos(pos, world_block)
        if(block.itemID == 25):
            gs.endGamePos = block.blockPosition
            gs.drawPortal = True

        if(block.itemID in ih.clickableBlocks):
            if(gs.drawCrafting):
                gs.drawCrafting = False
            else:
                gs.drawCrafting = True

        if block.itemID == -1:
            # Only allow placing if player has more blocks
            if (len(inv.invArray) != 0 and inv.getSelected().amount > 0):
                # Decrease inventory item

                # Add block to world
                if(textureNames.__contains__(itemIDs[inv.invArray[inv.selected].getItemId()])):
                    currTexture = textureNames[itemIDs[inv.invArray[inv.selected].getItemId()]]
                    if inv.invArray[inv.selected].isPlaceable:
                        tempBlock = Block(gs.blockSize, pos,  inv.invArray[inv.selected].getItemId(), currTexture, blockHardness[inv.invArray[inv.selected].getItemId()],breakTimes[inv.invArray[inv.selected].getItemId()])
                        # only added to world if block will not cause collision
                        if(not (player.willcollide(tempBlock))):
                            world_block.add(tempBlock)

                            gs.generatedChunks[gs.visibleChunks[1]].add(block)
                            inv.decrease()
                            #call sound effect
                            if(test==False and sound):
                                playBreakSoundforID(block.itemID)


def getBlockFromPos(pos, world_block):  # find block based on position in world
    for block in world_block:
        if block.blockPosition == pos:
            return block
    # if no block at position, return null block
    return Block(gs.blockSize, pos, -1,  textureNames["null"], 0, 99999)

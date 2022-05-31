import gameSettings as gs
import block
import inventoryHandler
import math
from block import Block
import inventoryHandler as inv
from soundHandler import playBreakSoundforID

def checkBreakable(block, inHand):
    # a block can only be broken if the current tool is harder than the block's hardness
    blockHardness = block.getHardness()
    itemHardness = inHand.getHardness()
    if(itemHardness >= blockHardness):
        return True
    else:
        return False


def notEmpty(hotbarSelected):
    if hotbarSelected.isEmpty():
        return False
    else:
        return True


# Block breaking logic, and inventory handler passover
def blockBreak(python_pos, world_block, player):
    if gs.distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = gs.getPos(python_pos)
        block = getBlockFromPos(pos, world_block)
        # find correct block to break. Check if block is breakable. i.e. not bed rock/ crafting table
        if(block.itemID != -1):
            if block.itemID not in gs.immovableBlocks and len(inv.invArray) > 0:
                if checkBreakable(block, inv.invArray[inv.selected]):
                    # Remove block from world
                    world_block.remove(block)
                    gs.generatedChunks[gs.visibleChunks[1]].remove(block)
                    # Add block to inventory
                    inv.addBlock(block)

                    #call sound effect
                    playBreakSoundforID(block.itemID)
            elif block.itemID not in gs.immovableBlocks:
                # payer is not holding a tool
                if block.getHardness() <= 0:
                    # Remove block from world
                    world_block.remove(block)
                    gs.generatedChunks[gs.visibleChunks[1]].remove(block)
                    # Add block to inventory
                    inv.addBlock(block)


# Block placing logic, and inventory handler requesting
def blockPlace(python_pos, world_block, player):
    if gs.distance(player, python_pos) <= gs.playerRange * gs.blockSize:
        pos = gs.getPos(python_pos)
        block = getBlockFromPos(pos, world_block)
        if(block.itemID == 25):
            gs.endGamePos = block.blockPosition
            gs.drawPortal = True

        if(block.itemID in gs.clickableBlocks):
            if(gs.drawCrafting):
                gs.drawCrafting = False
            else:
                gs.drawCrafting = True

        if block.itemID == -1:
            # Only allow placing if player has more blocks
            if (len(inv.invArray) != 0 and inv.getSelected().amount > 0):
                # Decrease inventory item

                # Add block to world
                if(gs.textureNames.__contains__(gs.itemIDs[inv.invArray[inv.selected].getItemId()])):
                    currTexture = gs.textureNames[gs.itemIDs[inv.invArray[inv.selected].getItemId()]]
                    if inv.invArray[inv.selected].isPlaceable:

                        tempBlock = Block(gs.blockSize, pos,  inv.invArray[inv.selected].getItemId(), currTexture, hardness=gs.blockHardness[inv.invArray[inv.selected].getItemId()])
                        # only added to world if block will not cause collision
                        if(not (player.willcollide(tempBlock))):
                            world_block.add(tempBlock)

                            gs.generatedChunks[gs.visibleChunks[1]].add(block)
                            inv.decrease()
                            playBreakSoundforID(block.itemID)

def getBlockFromPos(pos, world_block):  # find block based on position in world
    for block in world_block:
        if block.blockPosition == pos:
            return block
    # if no block at position, return null block
    return Block(gs.blockSize, pos, -1,  gs.textureNames["Null_Block"], 0)


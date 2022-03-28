import game_settings as gs
import math
from block import Block
import inventory_handler as inv

def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = gs.block_size*math.floor(pos[0]/gs.block_size),gs.block_size*math.floor(pos[1]/gs.block_size)
    return pos

def block_break(python_pos,world_block): #Block breaking logic, and inventory handler passover
    pos = getPos(python_pos)
    for block in world_block:
        if block.blockPosition == pos:
            #Add block to world
            world_block.remove(block)
            #Add block to inventory
            inv.add_block(block)


def block_place(python_pos,world_block): #Block placing logic, and inventory handler requesting
    pos = getPos(python_pos)
    found = False
    for block in world_block:
        if block.blockPosition == pos:
            found = True
    if found == False:

        #Only allow placing if player has more blocks
        if (inv.get_selected().amount >0):
            #Decrease inventory item
            inv.decrease()

            #Remove block from world
            temp_block = Block(gs.block_size, pos, gs.customColours[inv.get_selected().item_name])
            world_block.append(temp_block)


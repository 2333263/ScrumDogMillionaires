import game_settings as gs
import block
import inventory_handler
import math
from block import Block

def getPos(pos): #Takes in pygame position coordinates returns block coordinates
    pos = math.floor(pos[0]/gs.block_size),math.floor(pos[1]/gs.block_size)
    return pos

def block_break(python_pos,world_block):
    pos = getPos(python_pos)
    temp_block = Block(gs.block_size, (pos[0]*gs.block_size, pos[1]*gs.block_size), gs.customColours["sky"])
    for block in world_block:
        if block.blockPosition == temp_block.blockPosition:
            world_block.remove(block)
            block = temp_block
    #inventory TODO

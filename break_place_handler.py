import game_settings as gs
import block
import inventory_handler
import math
from block import Block

def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = gs.block_size*math.floor(pos[0]/gs.block_size),gs.block_size*math.floor(pos[1]/gs.block_size)
    return pos

def block_break(python_pos,world_block): #Block breaking logic, and inventory handler passover
    pos = getPos(python_pos)
    for block in world_block:
        if block.blockPosition == pos:
            world_block.remove(block)
    #inventory TODO

def block_place(python_pos,world_block): #Block placing logic, and inventory handler requesting
    pos = getPos(python_pos)
    found = False
    for block in world_block:
        if block.blockPosition == pos:
            found = True
    if found == False:
        temp_block = Block(gs.block_size, pos, gs.customColours["grass"])
        world_block.append(temp_block)   
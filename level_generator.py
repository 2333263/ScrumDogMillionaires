import pygame
import game_settings as gs
from block import Block

def getBlocks(level_name):
    block_array = []
    gs.level_name = level_name
    for i in range(len(gs.level_array)):
        for j in range(len(gs.level_array[i])):
            curr_height = i * gs.block_size
            curr_width = j * gs.block_size
            if(gs.level_array[i][j] == ' '):
                continue
            elif(gs.level_array[i][j] == 'G'):
                temp_block = Block(gs.block_size, (curr_width, curr_height), gs.customColours["grass"])
                block_array.append(temp_block)
            elif(gs.level_array[i][j] == 'S'):
                temp_block = Block(gs.block_size, (curr_width, curr_height), gs.customColours["stone"])
                block_array.append(temp_block)
            elif(gs.level_array[i][j] == 'C'):
                temp_block = Block(gs.block_size, (curr_width, curr_height), gs.customColours["cloud"])
                block_array.append(temp_block)   
    return block_array
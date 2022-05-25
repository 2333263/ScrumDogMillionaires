import random
import math
levelName = "random"
seed = random.randint(-10000, 10000) #-107
octaves = 1

with open('Levels/' + levelName + '.txt') as f:
    levelArray = f.readlines()


blockSize = 20 #tested values: [12, 16, 20,24, 32]otherwise collision issues (possibly all multiples of 4 work)
playerRange = 7
noXBlocks = 128
noYBlocks = int(9/16 * noXBlocks)
width = 1920
height = 1080

drawCrafting = False
craftingTablePos = [int(width/2) - 5 * blockSize, int(height/2) + 12 * blockSize]

endGamePos = [-1, -1]

#Moved to GS for global access
def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = blockSize*math.floor(pos[0]/blockSize),blockSize*math.floor(pos[1]/blockSize)
    return pos

#Moved to GS for global access
def distance(player, python_pos): #Takes in player position and coords and returns distance
    playerPos = getPos(player.getPlayerPos())
    blockPos = getPos(python_pos)
    return math.sqrt(pow((playerPos[0] - blockPos[0]), 2) + (pow((playerPos[1] - blockPos[1]), 2)))

#dictionary of all block types
itemIDs = {
   -1: "null",
    0 : "Grass",
    1 : "Dirt",
    2 : "Stone",
    3 : "Cloud",
    4 : "Bedrock",
    5 : "Crafting Table",
    6 : "Leaves",
    7 : "Logs",
    8 : "Wooden Planks",
    9 : "Crafting Background",
    10 : "Wooden Pickaxe",
    11 : "Stone Pickaxe",
    12 : "Stone Shovel",
    13 : "Coal Ore",
    14 : "Iron Ore",
    15 : "Gold Ore",
    16 : "Diamond Ore",
    17 : "Portal",
    18 : "Emerald Ore",
    19 : "Diamond",
    20 : "Emerald",
    21 : "Gold Ingot",
    22 : "Diamond Block",
    23 : "Emerald Block",
    24 : "Gold Block",
    25 : "End Game Block"
}
#dictionary of block hardnesses, correlating to itemIDs order
blockHardness = {
    -1: 0,
    0 : 0,
    1 : 0,
    2 : 0, #10
    3 : 999,
    4 : 999,
    5 : 999,
    6 : 0,
    7 : 0,
    8 : 0,
    9 : 999,
    10 : 0,
    11 : 0,
    12 : 0,
    13 : 10,
    14 : 15,
    15 : 15,
    16 : 0, #15
    17 : 999,
    18 : 20,
    22 : 20,
    23 : 20,
    24 : 20,
    25 : 999
}
#dictionary of tool hardness (strength) correlating to order of itemID dictionary
itemHardness = {
    -1: 0, #is a block, therefore has hardeness 0
    0 : 0,
    1 : 0,
    2 : 0,
    3 : 0,
    4 : 0,
    5 : 0,
    6 : 0,
    7 : 0,
    8 : 0,
    9 : 0,
    10 : 10, #tool with hardness level 10
    11 : 20, #tool
    12 : 20, #tool
    19 : 0,
    20 : 0,
    21 : 0
}
#dictionary controling whether an item can be placed into the world
#tools and ore cannot be placed into the world
#blocks can be pplaced into the world
isPlaceable = {
     -1: False,
    0 : True,
    1 : True,
    2 : True,
    3 : True,
    4 : True,
    5 : True,
    6 : True,
    7 : True,
    8 : True,
    9 : True,
    10 : False,
    11 : False,
    12 : False,
    13 : True,
    14 : True,
    15 : True,
    16 : True,
    17 : False,
    18 : True,
    19 : False,
    20 : False,
    21 : False,
    22 : True,
    23 : True,
    24 : True,
    25 : True
}


#IDs for the crafting table
#when json file is loaded into an array, say like data, data[0] will refer to the wooden planks recipe
#data[0]['toolName'] would return wooden planks 
craftingIDs = {
    0 : "Wooden Planks", 
    1 : "Wooden Pickaxe", 
    2 : "Stone Pickaxe",
    3 : "Stone Shovel",
    4 : "Diamond",
    5 : "Emerald",
    6 : "Gold Ingot",
    7 : "Diamond Block",
    8 : "Emerald Block",
    9 : "Gold Block",
    10 : "End Game Block"
}

converterIDs = {
    'G' : 0, #Grass
    'D' : 1, #Dirt
    'S' : 2, #Stone
    #'C' : 3, #Clouds
    'B' : 4, #Bedrock 
    'T' : 5, #Crafting Table
    'V' : 6, #Leaves 
    'L' : 7, #Logs,
    "C" : 13, #Coal Ore
    "I" : 14, #Iron Ore
    "A" : 15, #Gold Ore
    "M" : 16, #Diamond Ore
    "E" : 18, #Emerald Ore
    "O" : 22, #Diamond Block
    "R" : 23, #Emerald Block
    "U" : 24, #Gold Block
    "X" : 25 #End Game Block
}

textureNames = {
    #Blocks
    "Block_Frame" : "Textures/Blocks/block_frame.png",
    "Grass" : "Textures/Blocks/grass.png",
    "Stone" : "Textures/Blocks/stone.png",
    "Dirt" : "Textures/Blocks/dirt.png",
    "Cloud" : "Textures/Blocks/cloud.png",
    "Bedrock" : "Textures/Blocks/bedrock.png",
    "Crafting Table" : "Textures/Blocks/crafting.png",
    "Leaves" : "Textures/Blocks/leaves_dense.png",
    "Logs" : "Textures/Blocks/wood_log.png",
    "Crafting Background" : "Textures/Menus/crafting_background.png",
    "Wooden Planks" : "Textures/Blocks/wood_planks.png",
    "Coal Ore" : "Textures/Blocks/coal_ore.png",
    "Copper Ore" : "Textures/Blocks/copper_ore.png",
    "Gold Ore" : "Textures/Blocks/gold_ore.png",
    "Iron Ore" : "Textures/Blocks/iron_ore.png",
    "Diamond Ore" : "Textures/Blocks/diamond_ore.png",
    "Emerald Ore" : "Textures/Blocks/emerald_ore.png",
    "Twig Leaves" : "Textures/Blocks/leaves_twig.png",
    "Stone Bricks" : "Textures/Blocks/stone_bricks.png",
    "Diamond Block" :  "Textures/Blocks/diamond_block.png",
    "Emerald Block" : "Textures/Blocks/emerald_block.png",
    "Gold Block" : "Textures/Blocks/gold_block.png",
    "End Game Block" : "Textures/Blocks/end_game_block.png",

    #ITEMS:
    "Charcoal" : "Textures/Items/charcoal.png",
    "Diamond" : "Textures/Items/diamond.png",
    "Emerald" : "Textures/Items/emerald.png",
    "Flint" : "Textures/Items/flint.png",
    "Gold Ingot" : "Textures/Items/gold_ingot.png",
    "Iron Ingot" : "Textures/Items/iron_ingot.png",
    "Lapis Lazuli" : "Textures/Items/lapis_lazuli.png",
    "Netherite Ingot" : "Textures/Items/netherite_ingot.png",
    "Stick" : "Textures/Items/stick.png",
    
    #TOOLS:
    #fishingrods
    "Fishing Rod" : "Textures/Tools/fishing_rod.png",
    #wood
    "Wooden Sword" : "Textures/Tools/wooden_sword.png",
    "Wooden Shovel" : "Textures/Tools/wooden_shovel.png",
    "Wooden Pickaxe" : "Textures/Tools/wooden_pickaxe.png",
    "Wooden Hoe" : "Textures/Tools/wooden_hoe.png",
    "Wooden Axe" : "Textures/Tools/wooden_axe.png",
    #stone
    "Stone Sword" : "Textures/Tools/stone_sword.png",
    "Stone Shovel" : "Textures/Tools/stone_shovel.png",
    "Stone Pickaxe" : "Textures/Tools/stone_pickaxe.png",
    "Stone Hoe" : "Textures/Tools/stone_hoe.png",
    "Stone Axe" : "Textures/Tools/stone_axe.png",
    #netherite
    "Netherite Sword" : "Textures/Tools/netherite_sword.png",
    "Netherite Shovel" : "Textures/Tools/netherite_shovel.png",
    "Netherite Pickaxe" : "Textures/Tools/netherite_pickaxe.png",
    "Netherite Hoe" : "Textures/Tools/netherite_hoe.png",
    "Netherite Axe" : "Textures/Tools/netherite_axe.png",
    #iron
    "Iron Sword" : "Textures/Tools/iron_sword.png",
    "Iron Shovel" : "Textures/Tools/iron_shovel.png",
    "Iron Pickaxe" : "Textures/Tools/iron_pickaxe.png",
    "Iron Hoe" : "Textures/Tools/iron_hoe.png",
    "Iron Axe" : "Textures/Tools/iron_axe.png",
    #gold
    "Golden Sword" : "Textures/Tools/golden_sword.png",
    "Golden Shovel" : "Textures/Tools/golden_shovel.png",
    "Golden Pickaxe" : "Textures/Tools/golden_pickaxe.png",
    "Golden Hoe" : "Textures/Tools/golden_hoe.png",
    "Golden Axe" : "Textures/Tools/golden_axe.png",
    #diamond
    "Diamond Sword" : "Textures/Tools/diamond_sword.png",
    "Diamond Shovel" : "Textures/Tools/diamond_shovel.png",
    "Diamond Pickaxe" : "Textures/Tools/diamond_pickaxe.png",
    "Diamond Hoe" : "Textures/Tools/diamond_hoe.png",
    "Diamond Axe" : "Textures/Tools/diamond_axe.png",

    #MENUS
    "Sky" : "Textures/Screens/sky.png",
    "Crafting Background" : "Textures/Screens/CraftingMenu.png",
    "Portal" : "Textures/Screens/portal.png"
}
immovableBlocks = [3, 5] #list used to store itemIDs of blocks that cannot be moved
clickableBlocks = [5]

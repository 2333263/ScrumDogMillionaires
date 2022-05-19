import random
import math
levelName = "random"
seed = random.randint(-10000, 10000)
octaves = 1

with open('Levels/' + levelName + '.txt') as f:
    levelArray = f.readlines()


blockSize = 20 #tested values: [12, 16, 20,24, 32]otherwise collision issues (possibly all multiples of 4 work)
playerRange = 7
noXBlocks = 128
noYBlocks = int(9/16 * noXBlocks)
width = 1280
height = 720

drawCrafting = False
craftingTablePos = [int(width/2) - 5 * blockSize, int(height/2) + 12 * blockSize]

#Moved to GS for global access
def getPos(pos): #Takes in pygame position coordinates returns block coordinates based system ---> returns block_size*floor(pyPos/block_size) tuple transform
    pos = blockSize*math.floor(pos[0]/blockSize),blockSize*math.floor(pos[1]/blockSize)
    return pos

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
    12 : "Stone Shovel"
}

blockHardness = {
     -1: 0,
    0 : 0,
    1 : 0,
    2 : 10,
    3 : 999,
    4 : 999,
    5 : 999,
    6 : 0,
    7 : 0,
    8 : 0,
    9 : 999,
    10 : 0,
    11 : 0,
    12 : 0
}

itemHardness = {
    -1: 0,
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
    10 : 10,
    11 : 20,
    12 : 20
}

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
    12 : False
}


#IDs for the crafting table
#when json file is loaded into an array, say like data, data[0] will refer to the wooden planks recipe
#data[0]['toolName'] would return wooden planks 
craftingIDs = {
    0 : "Wooden Planks", 
    1 : "Wooden Pickaxe", 
    2 : "Stone Pickaxe",
    3 : "Stone Shovel" 
}

converterIDs = {
    'G' : 0, #Grass
    'D' : 1, #Dirt
    'S' : 2, #Stone
    #'C' : 3, #Clouds
    'B' : 4, #Bedrock 
    'T' : 5, #Crafting Table
    'V' : 6, #Leaves 
    'L' : 7 #Logs
}

textureNames = {
    #Blocks
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
    "Twig Leaves" : "Textures/Blocks/leaves_twig.png",
    "Stone Bricks" : "Textures/Blocks/stone_bricks.png",

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
    "Crafting Background" : "Textures/Screens/CraftingMenu.png"
}
immovableBlocks = [3, 5]
clickableBlocks = [5]

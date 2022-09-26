import math
import random

#sets seed taken from user text input or a random number if no seed is given
seed = 1

actionSpace = {
    "MOVEMENT" : [i for i in range(-1, 5, 1)] ,
    "WORLD" : [i for i in range(5, 25, 1)],
    "HOTBAR" : [i for i in range(25, 65, 1)],
    "CRAFTING" : [i for i in range(65, 75, 1)]
}
def setSeed(string):   
    global seed
    if len(string)!=0:
        seed = int(hasher(string))
    else:
        seed = random.randint(-10000, 10000)
    return seed

def hasher(string):
    hash=""
    for char in string:
        hash+=str(ord(char))
    return hash

octaves = 1


blockSize = 30 #tested values: [12, 16, 20,24, 32]otherwise collision issues (possibly all multiples of 4 work)
playerRange = 7

width = 1280
height = 720

generatedChunks = {}
CHUNK_SIZE = [34, 70]
visibleChunks = [-1, 0, 1]

drawCrafting = False
craftingTablePos = [int(width/2) - 5 * blockSize, int(height/2) + 12 * blockSize]

endGamePlaced = False
drawPortal = True
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
# itemIDs = {
#     # ALL COMMENTS ARE ITEMS IN NEW ITEM JSON AND ARE MISSING HERE
#    -1: "null",
#     0 : "Grass",
#     1 : "Dirt",
#     2 : "Stone",
#     3 : "Cloud",
#     4 : "Bedrock",
#     5 : "Crafting Table",
#     6 : "Leaves", #Oak
#     7 : "Logs", #Oak
#     8 : "Wooden Planks", #Oak
#     9 : "Crafting Background",
#     #10 is sky bugged in NEW JSON FORMAT
#     11 : "Wooden Pickaxe", #was 10
#     # More Sooden Tools
#     16 : "Stone Pickaxe", #was 11
#     # Stone Axe
#     18 : "Stone Shovel", #was 12
#     # More Stone Tools
#     # Gold Tools
#     # Iron Toolsz
#     # Diamond Tools
#     # Netherite Tools
#     41 : "Coal Ore", #was 13
#     43 : "Iron Ore", #was 14
#     46 : "Gold Ore", #was 15
#     49 : "Diamond Ore", #was 16
#     17 : "Portal", #was 17 ALSO WHAT DOES THIS DO (kept 17)
#     78 : "Emerald Ore", #was 18
#     50 : "Diamond", #was 19
#     53 : "Emerald", #was 20
#     47 : "Gold Ingot", #was 21
#     67 : "Diamond Block", #was 22
#     63 : "Emerald Block", #was 23
#     64 : "Gold Block", #was 24
#     83 : "End Game Block", #was 25
#     84 : "Portal Block" #was 26
# }

#dictionary of block hardnesses, correlating to itemIDs order
# blockHardness = {
#     -1: 0,
#     0 : 0,
#     1 : 0,
#     2 : 10, #10
#     3 : 999,
#     4 : 999,
#     5 : 999,
#     6 : 0,
#     7 : 0,
#     8 : 0,
#     9 : 999,
#     11 : 0,
#     16 : 0,
#     18 : 0,
#     41 : 10,
#     43 : 15,
#     46 : 15,
#     49 : 15,
#     84 : 999,
#     78 : 20,
#     67 : 20,
#     63 : 20,
#     64 : 20,
#     83 : 999,
#     84 : 999
# }
#dictionary of tool hardness (strength) correlating to order of itemID dictionary
# itemHardness = {
#     -1: 0,
#     0: 0,
#     1: 0,
#     2: 0,
#     3: 0,
#     4: 0,
#     5: 0,
#     6: 0,
#     7: 0,
#     8: 0,
#     9: 0,
#     11: 10,
#     16: 20,
#     18: 20,
#     41: 0,
#     43: 0,
#     46: 0,
#     49: 0,
#     84: 0,
#     78: 0,
#     50: 0,
#     53: 0,
#     47: 0,
#     67: 0,
#     63: 0,
#     64: 0,
#     83: 0,
#     84: 0,
# }
#dictionary controling whether an item can be placed into the world
#tools and ore cannot be placed into the world
#blocks can be pplaced into the world
# isPlaceable = {
#     -1: False,
#     0 : False,
#     1 : True,
#     2 : True,
#     3 : True,
#     4 : True,
#     5 : True,
#     6 : True,
#     7 : True,
#     8 : True,
#     9 : True,
#     11 : False,
#     16 : False,
#     18 : False,
#     41 : True,
#     43 : True,
#     46 : True,
#     49 : True,
#     84 : False,
#     78 : True,
#     50 : False,
#     53 : False,
#     47 : False,
#     67 : True,
#     63 : True,
#     64 : True,
#     83 : True,
#     84 : False
# }


#IDs for the crafting table
#when json file is loaded into an array, say like data, data[0] will refer to the wooden planks recipe
#data[0]['toolName'] would return wooden planks

# textureNames = {
#     #Ui Blocks
#     "Block_Frame" : "Textures/Blocks/block_frame.png",
#     "Block_Frame_Red" : "Textures/Blocks/block_frame_red.png",
#     "Block_Frame_Green" : "Textures/Blocks/block_frame_green.png",
#     "Null_Block" : "Textures/Blocks/null_block.png",
#     "Block_Frame_Green_1_4" : "Textures/Blocks/block_frame_green_1-4.png",
#     "Block_Frame_Green_2_4" : "Textures/Blocks/block_frame_green_2-4.png",
#     "Block_Frame_Green_3_4" : "Textures/Blocks/block_frame_green_3-4.png",
#     "Block_Frame_Green_4_4" : "Textures/Blocks/block_frame_green_4-4.png",
#
#
#     #normal blocks
#     "Grass" : "Textures/Blocks/grass.png",
#     "Stone" : "Textures/Blocks/stone.png",
#     "Dirt" : "Textures/Blocks/dirt.png",
#     "Cloud" : "Textures/Blocks/cloud.png",
#     "Bedrock" : "Textures/Blocks/bedrock.png",
#     "Crafting Table" : "Textures/Blocks/crafting.png",
#     "Leaves" : "Textures/Blocks/leaves_dense.png",
#     "Logs" : "Textures/Blocks/wood_log.png",
#     "Crafting Background" : "Textures/Menus/crafting_background.png",
#     "Wooden Planks" : "Textures/Blocks/wood_planks.png",
#     "Coal Ore" : "Textures/Blocks/coal_ore.png",
#     "Copper Ore" : "Textures/Blocks/copper_ore.png",
#     "Gold Ore" : "Textures/Blocks/gold_ore.png",
#     "Iron Ore" : "Textures/Blocks/iron_ore.png",
#     "Diamond Ore" : "Textures/Blocks/diamond_ore.png",
#     "Emerald Ore" : "Textures/Blocks/emerald_ore.png",
#     "Twig Leaves" : "Textures/Blocks/leaves_twig.png",
#     "Stone Bricks" : "Textures/Blocks/stone_bricks.png",
#     "Diamond Block" :  "Textures/Blocks/diamond_block.png",
#     "Emerald Block" : "Textures/Blocks/emerald_block.png",
#     "Gold Block" : "Textures/Blocks/gold_block.png",
#     "End Game Block" : "Textures/Blocks/end_game_block.png",
#     "Portal Block" : "Textures/Blocks/PortalBlock.png",
#
#     #ITEMS:
#     "Charcoal" : "Textures/Items/charcoal.png",
#     "Diamond" : "Textures/Items/diamond.png",
#     "Emerald" : "Textures/Items/emerald.png",
#     "Flint" : "Textures/Items/flint.png",
#     "Gold Ingot" : "Textures/Items/gold_ingot.png",
#     "Iron Ingot" : "Textures/Items/iron_ingot.png",
#     "Lapis Lazuli" : "Textures/Items/lapis_lazuli.png",
#     "Netherite Ingot" : "Textures/Items/netherite_ingot.png",
#     "Stick" : "Textures/Items/stick.png",
#
#     #TOOLS:
#     #fishingrods
#     "Fishing Rod" : "Textures/Tools/fishing_rod.png",
#     #wood
#     "Wooden Sword" : "Textures/Tools/wooden_sword.png",
#     "Wooden Shovel" : "Textures/Tools/wooden_shovel.png",
#     "Wooden Pickaxe" : "Textures/Tools/wooden_pickaxe.png",
#     "Wooden Hoe" : "Textures/Tools/wooden_hoe.png",
#     "Wooden Axe" : "Textures/Tools/wooden_axe.png",
#     #stone
#     "Stone Sword" : "Textures/Tools/stone_sword.png",
#     "Stone Shovel" : "Textures/Tools/stone_shovel.png",
#     "Stone Pickaxe" : "Textures/Tools/stone_pickaxe.png",
#     "Stone Hoe" : "Textures/Tools/stone_hoe.png",
#     "Stone Axe" : "Textures/Tools/stone_axe.png",
#     #netherite
#     "Netherite Sword" : "Textures/Tools/netherite_sword.png",
#     "Netherite Shovel" : "Textures/Tools/netherite_shovel.png",
#     "Netherite Pickaxe" : "Textures/Tools/netherite_pickaxe.png",
#     "Netherite Hoe" : "Textures/Tools/netherite_hoe.png",
#     "Netherite Axe" : "Textures/Tools/netherite_axe.png",
#     #iron
#     "Iron Sword" : "Textures/Tools/iron_sword.png",
#     "Iron Shovel" : "Textures/Tools/iron_shovel.png",
#     "Iron Pickaxe" : "Textures/Tools/iron_pickaxe.png",
#     "Iron Hoe" : "Textures/Tools/iron_hoe.png",
#     "Iron Axe" : "Textures/Tools/iron_axe.png",
#     #gold
#     "Golden Sword" : "Textures/Tools/golden_sword.png",
#     "Golden Shovel" : "Textures/Tools/golden_shovel.png",
#     "Golden Pickaxe" : "Textures/Tools/golden_pickaxe.png",
#     "Golden Hoe" : "Textures/Tools/golden_hoe.png",
#     "Golden Axe" : "Textures/Tools/golden_axe.png",
#     #diamond
#     "Diamond Sword" : "Textures/Tools/diamond_sword.png",
#     "Diamond Shovel" : "Textures/Tools/diamond_shovel.png",
#     "Diamond Pickaxe" : "Textures/Tools/diamond_pickaxe.png",
#     "Diamond Hoe" : "Textures/Tools/diamond_hoe.png",
#     "Diamond Axe" : "Textures/Tools/diamond_axe.png",
#
#     #MENUS
#     "Sky" : "Textures/Screens/sky.png",
#     "Crafting Background" : "Textures/Screens/CraftingMenu.png",
#     "Portal" : "Textures/Screens/portal.png"
# }
# immovableBlocks = [3, 5] #list used to store itemIDs of blocks that cannot be moved
# clickableBlocks = [5,83]

import unittest
from MainGame.Camera import Camera
# import item
from MainGame.Settings import gameSettings as gs
from MainGame.Blocks import block,breakPlaceHandler as bph
import pygame
from MainGame.Crafting import CraftButtonHandler,CraftingMenu
import TextHandler
from MainGame.Recipes import recipeHandler
from MainGame.Player import playerHandler as ph
from MainGame.Inventory import inventoryHandler as ih,InventorySlots
from MainGame.Chunks import ChunkGenerator as CG,ChunkHandler as CH
from MainGame.Portal import Portal
from MainGame.Items import itemHandler,itemNew
import numpy as np
import gym
import gym_MC
from MainGame.Rewards import rewardsHandler

# replaces gamesettings
# use itemIDs instead of gs.itemIDs
itemIDs = itemHandler.fetchItemIDs()
textureNames = itemHandler.fetchTextureNames()
isPlaceable = itemHandler.fetchIsPlaceable()
itemHardness = itemHandler.fetchItemHardness()
blockHardness = itemHandler.fetchBlockHardness()
craftingIDs = itemHandler.craftingIDs
converterIDs = itemHandler.converterIDs
immovableBlocks = itemHandler.immovableBlocks
clickableBlocks = itemHandler.clickableBlocks
breakSpeed = itemHandler.breakTime

itemArr = itemHandler.fetchDict()
# update test for sound

#tests that the item class's properties and types
class TestItem(unittest.TestCase):
    tempItem = itemArr[1]  # Item("Grass", 0)
    tempItem1 = itemArr[2]  # Item("Dirt", 0, 20)]
    tempItem1.itemHardness=20
    
    #tests that the item id properties and ranges is set correctly
    def test_itemID(self):
        self.assertIsInstance(self.tempItem.itemID, int) # itemID type is int
        self.assertGreaterEqual(self.tempItem.itemID, 0) # itemID is greater than 0
        self.assertLessEqual(self.tempItem.itemID, len(itemIDs) + 1) # itemID is less than the length of itemIDs
        self.assertEqual(self.tempItem.getItemId(), self.tempItem.itemID) # itemID is equal to the itemID of the item
        self.assertIsInstance(self.tempItem1.itemID, int) # itemID type is int
        self.assertGreaterEqual(self.tempItem1.itemID, 0) # itemID is greater than 0
        self.assertLessEqual(self.tempItem1.itemID, len(itemIDs) + 1) # itemID is less than the length of itemIDs
        self.assertEqual(self.tempItem1.getItemId(), self.tempItem1.itemID) # itemID is equal to the itemID of the item

    #tests that the item amount properties and ranges is set correctly
    def test_amount(self):
        self.assertIsInstance(self.tempItem.amount, int) # amount type is int
        self.assertGreaterEqual(self.tempItem.amount, 0) # amount is greater equal than 0
        self.assertIsInstance(self.tempItem1.amount, int) # amount type is int
        self.assertGreaterEqual(self.tempItem1.amount, 0) # amount is greater equal than 0
        oldCount = self.tempItem.amount
        self.tempItem.increase() # increase amount by 1
        self.assertGreaterEqual(self.tempItem.amount, oldCount) # amount is greater equal than oldCount
        self.tempItem.decrease() # decrease amount by 1
        self.assertEqual(self.tempItem.amount, oldCount) # amount is equal to oldCount
        self.assertEqual(self.tempItem.amount, self.tempItem.getCount()) # amount is equal to the amount of the item

    #tests that the item name properties and ranges is set correctly
    def test_name(self):
        self.assertIsInstance(self.tempItem.itemDisplayName, str) # itemDisplayName type is str
        self.assertEqual(self.tempItem.getItemName(), "Grass Block") # itemDisplayName is equal to the itemDisplayName of the item
        self.assertIsInstance(self.tempItem1.itemDisplayName, str) # itemDisplayName type is str
        self.assertEqual(self.tempItem1.getItemName(), "Dirt Block") # itemDisplayName is equal to the itemDisplayName of the item

    #tests that the item hardness properties and ranges is set correctly
    def test_Hardness(self):
        self.assertEqual(self.tempItem.getItemHardness(), 0) # itemHardness is equal to the correct itemHardness of the item
        self.assertEqual(self.tempItem1.getItemHardness(), 20) # itemHardness is equal to the correct itemHardness of the item

#test block's properties
class TestBlock(unittest.TestCase):
    tempBlock = block.Block(gs.blockSize,(0,0),0,textureNames[itemIDs[0]],0,breakSpeed[0]) 

    def test_itemIDs(self):
        self.assertIsInstance(self.tempBlock.itemID, int) # itemID type is int
        self.assertGreaterEqual(self.tempBlock.itemID, 0) # itemID is greater than 0
        self.assertLessEqual(self.tempBlock.itemID, len(itemIDs) + 1) # itemID is less than the length of itemIDs

    def test_positions(self):
        self.assertGreaterEqual(self.tempBlock.blockPosition[0], 0) # x position is greater equal  than 0
        self.assertGreaterEqual(self.tempBlock.blockPosition[1], 0)     # y position is greater equal  than 0  

        self.assertLessEqual(self.tempBlock.blockPosition[0], gs.width) # x position is less equal  than width
        self.assertLessEqual(self.tempBlock.blockPosition[1], gs.height)    # y position is less equal  than height

    def test_texture(self):
        self.assertIsInstance(self.tempBlock.textureName, str) # textureName type is str
        self.assertIsInstance(self.tempBlock.rect, pygame.rect.Rect) # rect type is pygame.rect.Rect

    def test_hardness(self):
        self.assertEqual(self.tempBlock.getHardness(), 0) # hardness is equal to 0

#tests realting to the button that does the crafts
class TestCraftingButton(unittest.TestCase):
    tempButton = CraftButtonHandler.Button(0,(0,0),50,50)
    pygame.init()
    #tests that the item id of the button is set correctly
    def test_itemIDs(self):
        self.assertIsInstance(self.tempButton.itemID, int)
        self.assertGreaterEqual(self.tempButton.itemID, 0)
        self.assertLessEqual(self.tempButton.itemID, len(itemIDs) + 1)
    #tests that the position of the button is set correctlt
    def test_positions(self):
        self.assertGreaterEqual(self.tempButton.pos[0], 0)
        self.assertGreaterEqual(self.tempButton.pos[1], 0)

        self.assertLessEqual(self.tempButton.pos[0], gs.width)
        self.assertLessEqual(self.tempButton.pos[1], gs.height)
    #tests that the buttons rect is set correctly (this is so collisions work)
    def test_rectangle(self):
        self.assertIsInstance(self.tempButton.rect, pygame.rect.Rect)

#tests that creation of text based sprites works
class TestTextHandler(unittest.TestCase):
    testText = TextHandler.Text("TestCase", 12, "red", (0, 0))
    #test that the text is set correctly
    def test_text(self):
        self.assertIsInstance(self.testText.words, str)
        self.assertIsInstance(self.testText.my_font, pygame.font.Font)
        self.assertIsInstance(self.testText.rect, pygame.rect.Rect)
    #tests that the position of the text is positioned correctly on screen
    def test_positions(self):
        self.assertGreaterEqual(self.testText.pos[0], 0)
        self.assertGreaterEqual(self.testText.pos[1], 0)

        self.assertLessEqual(self.testText.pos[0], gs.width)
        self.assertLessEqual(self.testText.pos[1], gs.height)

#tests that the recipehandler function's types
class TestRecipeHandler(unittest.TestCase):
    tempHandler = recipeHandler.RecipeHandler()
    #tests that the recipe handler is created correctly by checking correct types
    def test_initialiser(self):
        self.assertIsInstance(self.tempHandler.recipe, dict)

    def test_recipeInfo(self):
        self.assertIsInstance(self.tempHandler.getRecipeInfo(11), dict)

    def test_getRecipe(self):
        self.assertIsInstance(self.tempHandler.getRecipe(11), dict)

    def test_CraftingAmount(self):
        self.assertIsInstance(self.tempHandler.getCraftingAmount(11), int)

    def test_getItemIDs(self):
        self.assertIsInstance(self.tempHandler.getAllItemIDs(), list)

    def test_craftingShape(self):
        self.assertIsInstance(self.tempHandler.getCraftingShape(11), list)

#this group of tests, tests various complenents of the player
class TestPlayer(unittest.TestCase):
    TempPlayer = ph.Player((8 * gs.blockSize, 8 * gs.blockSize), 24)
    #test the creation of the player worked
    def test_innit(self):
        self.assertEqual(self.TempPlayer.rect.x, 8 * gs.blockSize)
        self.assertEqual(self.TempPlayer.rect.y, 8 * gs.blockSize)
        self.assertTrue(type(self.TempPlayer) is ph.Player)
    #test that the player spawnned in the correct location
    def test_pos(self):
        self.assertEqual(self.TempPlayer.getPlayerPos(), (8 * gs.blockSize, 8 * gs.blockSize))
    #tests the player moving left and right
    def test_MoveX(self):
        self.simulatedKeys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False
        }
        self.simulatedKeys[pygame.K_LEFT] = True #move left
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, -2) #check the player moved left
        self.simulatedKeys[pygame.K_LEFT] = False #stop moving left
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, 0) #check the player stopped moving

        self.simulatedKeys[pygame.K_a] = True #move left
        self.TempPlayer.MoveOnX(self.simulatedKeys)     #move the player
        self.assertEqual(self.TempPlayer.direction.x, -2) #check the player moved left
        self.simulatedKeys[pygame.K_a] = False #stop moving left
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, 0) #check the player stopped moving

        self.simulatedKeys[pygame.K_RIGHT] = True #move right
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, 2) #check the player moved right
        self.simulatedKeys[pygame.K_RIGHT] = False #stop moving right
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, 0) #check the player stopped moving

        self.simulatedKeys[pygame.K_d] = True #move right
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, 2) #check the player moved right 
        self.simulatedKeys[pygame.K_d] = False #stop moving right 
        self.TempPlayer.MoveOnX(self.simulatedKeys) #move the player
        self.assertEqual(self.TempPlayer.direction.x, 0)
    #tests that when the player is in the air, gravity pulls him down
    def test_gravity(self):
        self.TempPlayer.useGravity()
        self.assertEqual(self.TempPlayer.direction.y, self.TempPlayer.gravity)
        self.TempPlayer.direction.y = 0
    #tests that when the player jumps the characters moves up correctly and then falls back down correctly
    def test_jump(self):
        # jumped is false by default in case we spawn the player above the world
        self.assertEqual(self.TempPlayer.jumped, False)
        self.TempPlayer.jump()
        self.assertEqual(self.TempPlayer.jumped, True)
        self.assertEqual(self.TempPlayer.direction.y, -8.5)
        self.TempPlayer.jumped = False
    #tests that the player falls correctly
    def test_jumping_acceleration(self):
        self.TempPlayer.jumpArc()
        # check if player is jumped get set to false when direction.y==0
        self.assertEqual(self.TempPlayer.jumped, False)
        self.TempPlayer.direction.y = -5
        # testing if the grabity acceleration changes
        self.TempPlayer.jumpArc()
        self.assertEqual(self.TempPlayer.direction.y, -5 + self.TempPlayer.gravity / 5)
        self.TempPlayer.direction.y = 0

    #tests the following:
    # 1) given a change in veclocity the player will move in that direction
    # 2) given the player is in the air, he will slow down and eventually fall
    # 3) given the player is falling, given there is a block under neath him he will stop falling
    # 4) given the player is moving in a direction, if he collides with a block he cannot go through it and it stops him from moving in that direction
    # 5) tests collision
    def test_update(self):
        tempBlock = block.Block(gs.blockSize,(8,7),0,textureNames[itemIDs[0]],0,breakSpeed[0]) #create a block
        tempGroup = pygame.sprite.Group() #create a group
        tempGroup.add(tempBlock) #add the block to the group
        self.TempPlayer.jumped = True #set jumped to true
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.jumped, False) #check that jumped is now false
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.y, 4.0) #check that the player is falling
        for x in tempGroup:
            x.blockPosition = (8 * gs.blockSize, 10 * gs.blockSize) #move the block under the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.y, 4.0) #check that the player is falling
        self.TempPlayer.direction.x = -1 #move the player left
        for x in tempGroup:
            x.blockPosition = (7 * gs.blockSize, 8 * gs.blockSize) #move the block to the left of the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.x, -1.0) #check that the player is moving left
        self.TempPlayer.direction.x = -1 #move the player left
        for x in tempGroup:
            x.blockPosition = (7 * gs.blockSize, 9 * gs.blockSize) #move the block to the left of the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.x, -1.0) #check that the player is moving left
        self.TempPlayer.direction.x = 1 #move the player right
        for x in tempGroup:
            x.blockPosition = (9 * gs.blockSize, 8 * gs.blockSize) #move the block to the right of the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.x, 1.0) #check that the player is moving right
        self.TempPlayer.direction.x = 1 #move the player right
        for x in tempGroup:
            x.blockPosition = (9 * gs.blockSize, 9 * gs.blockSize)  #move the block to the right of the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.x, 1.0) #check that the player is moving right
        self.TempPlayer.jumped = True #set jumped to true
        for x in tempGroup:
            x.blockPosition = (8 * gs.blockSize, 8 * gs.blockSize) #move the block under the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.direction.y, 4.8) #check that the player is falling
        self.TempPlayer.direction.x = 1 #move the player right
        self.TempPlayer.direction.y = 1 #move the player down
        tempPosX = self.TempPlayer.rect.x #store the players x position
        tempPosY = self.TempPlayer.rect.y #store the players y position
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.rect.y, tempPosY + 1) #check that the player moved down
        self.assertEqual(self.TempPlayer.rect.x, tempPosX + 1) #check that the player moved right
        self.TempPlayer.rect.x = tempPosX #reset the players x position
        self.TempPlayer.rect.y = tempPosY #reset the players y position
        self.TempPlayer.update(2, tempGroup) #update the player
        self.assertEqual(self.TempPlayer.rect.y, tempPosY + 5) #check that the player moved down
        self.assertEqual(self.TempPlayer.rect.x, tempPosX + 2) #check that the player moved right
        tempBlock = block.Block(gs.blockSize,(8 * gs.blockSize,7 * gs.blockSize),0,textureNames[itemIDs[0]],
                                0,breakSpeed[0]) #create a block
        tempGroup.add(tempBlock) #add the block to the group
        self.TempPlayer.rect.x = 8 * gs.blockSize - 1 #move the player to the left of the block
        self.TempPlayer.rect.y = 7 * gs.blockSize #move the player to the top of the block
        self.TempPlayer.direction.x = 1 #move the player right

        self.TempPlayer.update(1, tempGroup) #update the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(8 * gs.blockSize - 1, self.TempPlayer.rect.x) #check that the player is not moving right
        self.TempPlayer.rect.x = 8 * gs.blockSize + 1 #move the player to the right of the block
        self.TempPlayer.rect.y = 7 * gs.blockSize #move the player to the top of the block
        self.TempPlayer.direction.x = -1 #move the player left
        self.TempPlayer.update(1, tempGroup) #update the player
        self.TempPlayer.update(0, tempGroup) #update the player
        self.assertEqual(8 * gs.blockSize + 1, self.TempPlayer.rect.x) #check that the player is not moving left
        self.TempPlayer.jumped = True #set jumped to true
        self.TempPlayer.rect.x = 8 * gs.blockSize #move the player to the left of the block
        self.TempPlayer.rect.y = 7 * gs.blockSize #move the player to the top of the block
        self.TempPlayer.direction.y = -3 #move the player up
        self.TempPlayer.update(1, tempGroup) #update the player
        self.assertEqual(tempBlock.rect.bottom, self.TempPlayer.rect.top) #check that the player is on top of the block
        self.assertFalse(self.TempPlayer.jumped) #check that jumped is false
        self.TempPlayer.rect.x = 8 * gs.blockSize #move the player to the left of the block
        self.TempPlayer.rect.y = 7 * gs.blockSize - 1 #move the player to the top of the block
        self.TempPlayer.direction.y = 3 #move the player down

        self.TempPlayer.update(1, tempGroup) #update the player
        self.assertEqual(tempBlock.rect.top, self.TempPlayer.rect.bottom) #check that the player is under the block

    #tests that when the user stops moving the player, the player stops moving
    def test_StopOnX(self):
        self.TempPlayer.stopMoveOnX()
        self.assertEqual(self.TempPlayer.direction.x, 0)
    #test that when the player collides witha a block they stop moving
    def test_willcolide(self):
        tempBlock = block.Block(gs.blockSize,(8,7),0,textureNames[itemIDs[0]],0,breakSpeed[0])
        tempGroup = pygame.sprite.Group() #create a group
        tempGroup.add(tempBlock) #add the block to the group

        self.TempPlayer.rect.x = 8 #move the player to the left of the block
        self.TempPlayer.rect.y = 7 #move the player to the top of the block
        self.assertTrue(self.TempPlayer.willcollide(tempBlock)) #check that the player will collide with the block
        self.TempPlayer.rect.x = 22 * gs.blockSize #move the player to the right of the block
        self.TempPlayer.rect.y = 22 * gs.blockSize #move the player to the bottom of the block
        self.assertFalse(self.TempPlayer.willcollide(tempBlock)) #check that the player will not collide with the block

#tests involving the crafting menu
class TestCraftingMenu(unittest.TestCase):
    screen = pygame.display
    crafter = CraftingMenu.Crafting(screen)
    #tests that the ininilziation of the crafting menu works
    def test_innit(self):  # I had to call it AAinit so it would run before the other test cases
        self.crafter.initGroup()
        self.assertIsInstance(CraftingMenu.slots,pygame.sprite.Group)
        self.assertEqual(len(CraftingMenu.slots),10)
    #tests that the menu will scale with the window
    def test_relativeSize(self):
        self.assertTrue(self.crafter.relativeSize >= 0 and self.crafter.relativeSize <= gs.blockSize * 3)
    #tests that the crafter gets a list of all craftable items
    def test_allItems(self):
        self.assertIsInstance(list(), type(self.crafter.allItems))
    #tests that the empty crafting table function empties the crafting table
    def test_emptyTable(self):
        NullItem = itemArr[0]  # Null item, id -1
        self.crafter.emptyTable()
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.crafter.craftArray[i][j].itemID, -1)
        self.assertEqual(self.crafter.canCraft, False)
        self.assertEqual(self.crafter.craftID, -1)
    #checks that when given a valid crafting reciepie the crafting table detects it
    #also checks that the crafting table does not detect invalid recepies as valid
    def test_checkCanCraft(self):
        self.crafter.emptyTable()
        self.crafter.checkCanCraft()
        self.assertEqual(self.crafter.canCraft, False)
        self.assertEqual(self.crafter.craftID, -1)
        self.crafter.craftArray[1][1] = itemArr[8]  # Item("Logs", 7)
        self.crafter.checkCanCraft()
        self.assertEqual(self.crafter.canCraft, True)
        self.assertEqual(self.crafter.craftID, 8)
    #tests that when given a valid recipie the items are deleted and the crafted item is placed in the players invetory
    def test_doCraft(self):
        NullItem = itemArr[0]  # Null item, id -1
        self.crafter.emptyTable()
        self.crafter.doCraft()
        self.assertEqual(self.crafter.canCraft, False) # check that the craft is not valid because the table is empty
        self.assertEqual(self.crafter.craftID, -1) # check that the craft is not valid because the table is empty
        self.crafter.craftArray[1][1] = itemArr[8]  # Item("Logs", 7)
        ih.invArray = np.full(40,NullItem,dtype=itemNew.Item) #fill the inventory with null items
        curr = ih.getItemCount(8) #get the current number of logs
        self.crafter.doCraft() #craft the item
        self.assertEqual(ih.getItemCount(8), curr + 4) #check that the number of logs has increased by 4
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.crafter.craftArray[i][j].itemID, -1) #check that the crafting table is empty
        self.assertEqual(self.crafter.canCraft, False) #check that the craft is not valid because the table is empty
        self.assertEqual(self.crafter.craftID, -1) #check that the craft is not valid because the table is empty
        self.crafter.craftArray[1][1] = itemArr[47]  # Item("Gold Ore", 46)
        curr = ih.getItemCount(47) #get the current number of gold ore
        self.crafter.doCraft() #craft the item
        self.assertEqual(ih.getItemCount(47), curr + 1) #check that the number of gold ore has increased by 1
        ih.invArray = np.full(40,NullItem,dtype=itemNew.Item) #fill the inventory with null items
        for i in itemArr:
            if(i.amount>0):
                i.amount=0
    #same as the above 3 tests, but this is commbined for when the gym agent crafts             
    def testCraftSpec(self):
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                                blockHardness[7],breakSpeed[7])
        ih.addBlock(tempBlock)
        self.assertFalse(self.crafter.craftSpec(7, ih.getInv()))  # tries to craft gold, should fail
        self.assertFalse(self.crafter.craftSpec(-1, ih.getInv()))  # tries to craft a fake block, should fail
        self.assertFalse(self.crafter.craftSpec(0, {}))  # tries to craft planks with empty inventory
        self.assertTrue(self.crafter.craftSpec(0, ih.getInv()))  # tries to craft wooden planks should work
        self.assertFalse(
            self.crafter.craftSpec(1, ih.getInv()))  # tries to craft a pickaxe without enough wood, should fail
        ih.addBlock(tempBlock)  # add more logs
        self.crafter.craftSpec(0, ih.getInv())  # add more planks
        self.assertTrue(self.crafter.craftSpec(1, ih.getInv()))  # tries to craft pick now with enough wood, should pass
        inv = ih.getInv()
        for i in range(len(inv)):
            while (inv[i].getItemId() != -1):
                ih.decreaseSpec(inv[i].getItemId())
    
#tests that game settings intilizes correctly
class TestGameSettings(unittest.TestCase):
    def test_properties(self):
        self.assertIsInstance(gs.blockSize, int) # checks that the block size is an int
        self.assertGreaterEqual(gs.blockSize, 1) # checks that the block size is greater than 1

        self.assertIsInstance(gs.playerRange, int) # checks that the player range is an int
        self.assertGreaterEqual(gs.playerRange, 1) # checks that the player range is greater equal than 1

        self.assertIsInstance(gs.width, int) # checks that the width is an int
        self.assertGreaterEqual(gs.width, 1) # checks that the width is greater equal than 1
        self.assertIsInstance(gs.height, int) # checks that the height is an int
        self.assertGreaterEqual(gs.height, 1) # checks that the height is greater equal than 1

        self.assertIsInstance(gs.drawCrafting, bool) # checks that the draw crafting is a bool

        self.assertIsInstance(gs.craftingTablePos[0], int) # checks that the crafting table x position is an int
        self.assertGreaterEqual(gs.craftingTablePos[0], 1) # checks that the crafting table x position is greater equal than 1
        self.assertIsInstance(gs.craftingTablePos[1], int) # checks that the crafting table y position is an int
        self.assertGreaterEqual(gs.craftingTablePos[1], 1) # checks that the crafting table y position is greater equal than 1

        self.assertIsInstance(itemIDs, dict) # checks that the item ids is a dict
        self.assertIsInstance(craftingIDs, dict) # checks that the crafting ids is a dict
        self.assertIsInstance(converterIDs, dict) # checks that the converter ids is a dict
        self.assertIsInstance(textureNames, dict) # checks that the texture names is a dict

        self.assertIsInstance(immovableBlocks, list) # checks that the immovable blocks is a list
        self.assertIsInstance(clickableBlocks, list) # checks that the clickable blocks is a list

#tests involving the players inventory 
class TestInv(unittest.TestCase):
    #tests that the intilization works correctly
    def testAAInit(self):  # I had to call it AAinit so it would run before the other test cases
        inventory = ih.getInv() # gets the inventory
        empty = True # sets empty to true
        for i in inventory:
            if (i.getItemId() != -1):
                empty = False 
        self.assertTrue(empty) # checks that the inventory is empty
        ih.initGroup() # initializes the inventory
        self.assertIsInstance(ih.slots, pygame.sprite.Group) # checks that the slots are a group
        self.assertEqual(len(ih.slots), 40) # checks that there are 40 slots
        ih.selected = 0
        self.assertEqual(ih.getSelected().getItemId(), 5)
    #tests that blocks get added and removed from the players inventory correctly
    def testAddBlockandRemove(self):
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                                blockHardness[7],breakSpeed[7])
        ih.addBlock(tempBlock) # adds a block to the inventory
        found = False # sets found to false
        foundPos = 0 # sets foundPos to 0
        inv = ih.getInv() # gets the inventory
        for i in range(len(inv)):
            if (inv[i].getItemId() == 7):
                foundPos = i # sets foundPos to the position of the block
                found = True # sets found to true
        self.assertTrue(found) # checks that the block was found
        self.assertEqual(inv[foundPos].getCount(), 1) # checks that the count of the block is 1
        ih.addBlock(tempBlock) # adds another block to the inventory
        self.assertEqual(inv[foundPos].getCount(), 2) # checks that the count of the block is 2 
        ih.selected = foundPos # sets the selected slot to the position of the block
        ih.decrease() # decreases the count of the block
        self.assertEqual(inv[foundPos].getCount(), 1) # checks that the count of the block is 1
        ih.decrease() # decreases the count of the block
        self.assertEqual(inv[foundPos].getItemId(), -1) # checks that the block is no longer in the inventory
    #tests that when a specific item id is decremeneted it, gets decremented correctly from the players inventory
    def testDecSpec(self):
        inv = ih.getInv()
        self.assertEqual(inv[0].getItemId(), 5)  # crafting table is in position 0
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                                blockHardness[7],breakSpeed[7])
        ih.addBlock(tempBlock)  # should be in position 1
        inv = ih.getInv()
        self.assertEqual(inv[1].getItemId(), 7)
        ih.selected = 0
        ih.decreaseSpec(7)
        self.assertEqual(inv[1].getItemId(), -1)
    #tests that adding items works correctly
    def testAddItem(self):
        found = False # sets found to false
        inv = ih.getInv() # gets the inventory
        for i in inv:
            if (i.getItemId() == 11):
                found = True # sets found to true
        self.assertFalse(found) # checks that the item was not found
        tempItem = itemArr[12]  # Item("Wooden Pickaxe", 11)
        ih.addItem(tempItem) # adds the item to the inventory
        ih.addItem(tempItem) # adds the item to the inventory
        found = False # sets found to false
        inv = ih.getInv() # gets the inventory
        for i in inv:
            if (i.getItemId() == 11):
                found = True # sets found to true
        self.assertTrue(found) # checks that the item was found
        foundpos = 0 # sets foundpos to 0
        inv = ih.getInv() # gets the inventory
        for i in range(len(inv)): 
            if (inv[i].getItemId() == 11):
                foundpos = i # sets foundpos to the position of the item
        self.assertEqual(inv[foundpos].getCount(), 2)
        ih.decreaseSpec(11) # decreases the count of the item
        ih.decreaseSpec(11) # decreases the count of the item
    #tests that selecting a slot by various means all work correctly
    def testSelection(self):
        ih.selected = 0   # crafting table is in position 0          
        ih.selectNext() # selects the next slot
        self.assertEqual(ih.selected, 1) # checks that the selected slot is 1
        ih.selected = 9 # sets the selected slot to 9
        ih.selectNext() # selects the next slot
        self.assertEqual(ih.selected, 0) # checks that the selected slot is 0
        ih.selectPrevious() # selects the previous slot
        self.assertEqual(ih.selected, 9) # checks that the selected slot is 9
        ih.selectPrevious() # selects the previous slot
        self.assertEqual(ih.selected, 8) # checks that the selected slot is 8
        ih.selectInventory(7) # selects the slot at position 7
        self.assertEqual(ih.selected, 7) # checks that the selected slot is 7
        ih.selected = 0
    #tests that an item count is returned correctly
    def testGetitemCount(self):
        self.assertEqual(ih.getItemCount(5), 1)
        self.assertEqual(ih.getItemCount(14), 0)
    #tests that when clicking a slot that slot becomes selected
    #also tests that when 2 slots are selected when the inv is open, those items are swapped
    def testClick(self):
        ih.fullInv = False
        ih.selected = 0
        self.assertEqual(ih.selected, 0) # checks that the selected slot is 0
        ih.onClick((12 * ih.relative + 3 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.selected, 3) # checks that the selected slot is 3
        ih.fullInv = True
        self.assertEqual(ih.getClicked(), -1) # checks that the clicked slot is -1
        ih.onClick((12 * ih.relative + 0 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.clicked, 0) # checks that the clicked slot is 0
        ih.onClick((12 * ih.relative + 3 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.getClicked(), -1) # checks that the clicked slot is -1
        foundPos = 0
        inv = ih.getInv()
        for i in range(len(inv)): 
            if (inv[i].getItemId() == 5):
                foundPos = i # sets foundPos to the position of the block
        self.assertEqual(foundPos, 3) # checks that the block is in position 3
        ih.onClick((12 * ih.relative + 0 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.clicked, 0) # checks that the clicked slot is 0
        ih.onClick((12 * ih.relative + 3 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.clicked, -1) # checks that the clicked slot is -1
        ih.setClicked() # sets the clicked slot to -1
        self.assertEqual(ih.getClicked(), -1)

#tests functions related to the camera
class TestCamera(unittest.TestCase):
    TempPlayer = ph.Player((8 * gs.blockSize, 8 * gs.blockSize), 24) # creates a player
    Cam = Camera.Camera(TempPlayer) # creates a camera
    screen = pygame.Surface((gs.blockSize, gs.blockSize)) # creates a screen
    tempBlock = block.Block(gs.blockSize,(8,7),0,textureNames[itemIDs[0]],0,breakSpeed[0])
    tempBlock2 = block.Block(gs.blockSize,(20,7),1,textureNames[itemIDs[1]],0,breakSpeed[1])
    tempBlock3 = block.Block(gs.blockSize,(29,7),2,textureNames[itemIDs[1]],0,breakSpeed[2])
    tempBlock4 = block.Block(gs.blockSize,(50,7),3,textureNames[itemIDs[1]],0,breakSpeed[3])

    #tests that when the player moves, the camera follows them correctly
    def test_Offset(self):
        self.Cam.scroll()
        self.assertEqual(self.Cam.getOffsets(), self.Cam.offset)
    #tests that the only blocks the player can collide with are the blocks the camera can see
    def test_Collide(self):
        self.assertFalse(self.Cam.isColideable(self.tempBlock))
        self.tempBlock.rect.x = 8 * gs.blockSize
        self.tempBlock.rect.y = 8 * gs.blockSize
        self.assertTrue(self.Cam.isColideable(self.tempBlock))
    #tests that the only blocks loaded are the ones on screen
    def test_onScreen(self):
        self.assertTrue(self.Cam.isOnScreen(self.tempBlock))
        self.tempBlock.rect.x = 1000
        self.tempBlock.rect.y = 1000
    #tests that the blitting to the screen wroks correctly
    def test_draw(self):
        self.tempBlock.rect.x = 8 * gs.blockSize
        self.tempBlock.rect.y = 8 * gs.blockSize
        tempGroup = pygame.sprite.Group()
        tempGroup.add(self.tempBlock)
        tempGroup.add(self.tempBlock2)
        tempGroup.add(self.tempBlock3)
        tempGroup.add(self.tempBlock4)
        self.assertEqual(self.Cam.draw(self.screen, tempGroup), [self.tempBlock])

#tests related to handling of chunks
class testChunks(unittest.TestCase):
    testWorld = pygame.sprite.Group()
    TempPlayer = ph.Player((gs.width / 2 - gs.blockSize * 4,
                            - gs.blockSize * 2), 24)
    #tests that the chunks are generated correctly
    def test_generation(self):
        gs.generatedChunks[-1] = CG.generateChunk(-gs.CHUNK_SIZE[0], self.testWorld)
        gs.generatedChunks[0] = CG.generateChunk(0, self.testWorld)
        gs.generatedChunks[1] = CG.generateChunk(gs.CHUNK_SIZE[0], self.testWorld)
        self.assertIsInstance(gs.generatedChunks[-1], pygame.sprite.Group)
        self.assertIsInstance(gs.generatedChunks[0], pygame.sprite.Group)
        self.assertIsInstance(gs.generatedChunks[1], pygame.sprite.Group)
    #tests that when the player moves to the next chunk, the chunk off screen unloads and a new chunk loads in
    def test_Load_Unload(self):
        gs.generatedChunks[-1] = CG.generateChunk(-gs.CHUNK_SIZE[0], self.testWorld) # generates a chunk
        gs.generatedChunks[0] = CG.generateChunk(0, self.testWorld) # generates a chunk
        gs.generatedChunks[1] = CG.generateChunk(gs.CHUNK_SIZE[0], self.testWorld) # generates a chunk
        testChunk = [-1, 0, 1] # creates a list of the chunks
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld) # checks if the chunks need to be updated
        self.assertEqual(testChunk, gs.visibleChunks) # checks that the chunks are the same
        self.TempPlayer.rect.x += gs.CHUNK_SIZE[0] * gs.blockSize # moves the player to the next chunk
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld) # checks if the chunks need to be updated
        self.assertNotEqual(testChunk, gs.visibleChunks) # checks that the chunks are not the same
        self.assertEqual([0, 1, 2], gs.visibleChunks) # checks that the chunks are the same
        self.TempPlayer.rect.x -= gs.CHUNK_SIZE[0] * gs.blockSize   # moves the player to the previous chunk
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld) # checks if the chunks need to be updated
        self.assertEqual(testChunk, gs.visibleChunks) # checks that the chunks are the same
        self.TempPlayer.rect.x -= gs.CHUNK_SIZE[0] * gs.blockSize # moves the player to the previous chunk
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld) # checks if the chunks need to be updated
        self.assertNotEqual(testChunk, gs.visibleChunks) # checks that the chunks are not the same
        self.assertEqual([-2, -1, 0], gs.visibleChunks) # checks that the chunks are the same 
        self.TempPlayer.rect.x -= gs.CHUNK_SIZE[0] * gs.blockSize # moves the player to the previous chunk
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld) # checks if the chunks need to be updated
        self.assertNotEqual(testChunk, gs.visibleChunks) # checks that the chunks are not the same
        self.assertEqual([-3, -2, -1], gs.visibleChunks) # checks that the chunks are the same

#tests related to breaking and placing of blocks
class TestBreakPlace(unittest.TestCase):
    TempPlayer = ph.Player((8 * gs.blockSize, 8 * gs.blockSize), 24)
    pos = (8, 8)
    tempBlock = block.Block(gs.blockSize,(8 * gs.blockSize,7 * gs.blockSize),0,textureNames[itemIDs[0]],
                            1,breakSpeed[0])
    tempItem = itemArr[12]  # Item("Wooden Pickaxe", 11)
    tempItem.itemHardness = 3
    spriteGroup = pygame.sprite.Group()
    spriteGroup.add(tempBlock)
    
    #test tes function that takes in mouse coordinates and returns world coordinates
    def test_getPos(self):
        self.assertEqual(gs.getPos(self.pos), (0, 0))
    #tests if the player is holding a good enough tool they can break a given block
    #else they cannot break a given block
    def test_checkBreak(self):
        self.assertTrue(bph.checkBreakable(self.tempBlock, self.tempItem))
        self.tempItem.itemHardness = 0
        self.assertFalse(bph.checkBreakable(self.tempBlock, self.tempItem))
        self.tempItem.itemHardness = 11 #change itemhardness back --> NB need for rewards testing

    #testing that a block can be broken by the player, when they are able to (ie theyre holding a good enough tool)
    #then that block gets placed into the inv
    #else that they cannot break the block
    def test_breakBlock(self):
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),0,textureNames["Grass Block"],
                                blockHardness[0],breakSpeed[0]) #creates a block
        self.spriteGroup.add(tempBlock) #adds the block to the sprite group
        gs.generatedChunks[0] = self.spriteGroup #adds the sprite group to the chunk
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #breaks the block
        inventory = ih.getInv() #gets the inventory
        found = False #sets found to false
        for i in range(len(inventory)):
            if (inventory[i].itemID == 0 and inventory[i].getCount() == 1):
                ih.selected = i #sets the selected item to the item that was just added
                ih.decrease() #decreases the count of the item
                found = True #sets found to true
        self.assertTrue(found) #checks that the item was found
        tempBlock = block.Block(gs.blockSize,(30 * gs.blockSize,30 * gs.blockSize),0,textureNames["Grass Block"],
                                blockHardness[0],breakSpeed[0]) 
        self.spriteGroup.add(tempBlock) #adds the block to the sprite group
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        inventory = ih.getInv() #gets the inventory
        found = False #sets found to false
        for i in range(len(inventory)):
            if (inventory[i].itemID == 0 and inventory[i].getCount() == 1):
                found = True #sets found to true
        self.assertFalse(found) #checks that the item was not found
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"], 
                                blockHardness[2],breakSpeed[2])     #creates a block
        self.spriteGroup.add(tempBlock) #adds the block to the sprite group
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #breaks the block
        inventory = ih.getInv() #gets the inventory
        found = False #sets found to false
        for i in range(len(inventory)):
            if (inventory[i].itemID == 2 and inventory[i].getCount() == 1):
                found = True #sets found to true
        self.assertFalse(found)
        tempItem = itemArr[12]  # Item("Wooden Pickaxe", 11) #creates a pickaxe
        ih.addItem(tempItem) #adds the pickaxe to the inventory
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #breaks the block
        inventory = ih.getInv() #gets the inventory
        found = False #sets found to false
        for i in range(len(inventory)):
            if (inventory[i].itemID == 2 and inventory[i].getCount() == 1): #checks that the item was found
                ih.decreaseSpec(tempItem.itemID) #decreases the count of the item
                ih.selected = i #sets the selected item to the item that was just added
                ih.decrease() #decreases the count of the item
                found = True #sets found to true
        self.assertTrue(found) #checks that the item was found

    #test that when given a block in the world, we can get the item version of that block
    def test_getBlockFromPos(self):
        craftableBlock = block.Block(gs.blockSize,(10 * gs.blockSize,10 * gs.blockSize),5,
                                     textureNames[itemIDs[0]],1,breakSpeed[5])
        self.spriteGroup.add(craftableBlock)
        self.assertEqual(craftableBlock.itemID,
                         bph.getBlockFromPos((10 * gs.blockSize, 10 * gs.blockSize), self.spriteGroup).itemID)
        self.assertEqual(-1, bph.getBlockFromPos((200 * gs.blockSize, 10 * gs.blockSize), self.spriteGroup).itemID)

    #test that if the player is placing a block in a valid position (ie an empty spot)
    #that block gets removed from the inv and placed into the world
    def test_blockPlace(self):

        craftableBlock = block.Block(gs.blockSize,(10 * gs.blockSize,10 * gs.blockSize),5,
                                     textureNames[itemIDs[0]],1,breakSpeed[5]) #creates a block
        self.spriteGroup.add(craftableBlock) #adds the block to the sprite group
        bph.blockPlace(self.pos, self.spriteGroup, self.TempPlayer, True) #places the block
        self.assertFalse(gs.drawCrafting) #checks that the crafting menu is not open
        bph.blockPlace((craftableBlock.rect.x, craftableBlock.rect.y), self.spriteGroup, self.TempPlayer, True) #places the block
        self.assertTrue(gs.drawCrafting) #checks that the crafting menu is open
        self.pos = (8000, 8000) #sets the position to a position that is not in the world
        bph.blockPlace(self.pos, self.spriteGroup, self.TempPlayer, True) #places the block
        # empties the inventory
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            ih.selected = i #sets the selected item to the item that was just added
            if (ih.getSelected().itemID != -1): #checks that the item is not empty
                for j in range(ih.getSelected().getCount()): #loops through the count of the item
                    ih.decrease() #decreases the count of the item
        ih.selected = 0 #sets the selected item to the item that was just added
        gs.generatedChunks[0] = self.spriteGroup #adds the sprite group to the chunk
        tempBlock = block.Block(gs.blockSize,(15 * gs.blockSize,15 * gs.blockSize),43,textureNames["Iron Ore"],
                                blockHardness[43],breakSpeed[43]) #creates a block
        ih.addBlock(tempBlock) #adds the block to the inventory
        self.TempPlayer.rect.x = 8 * gs.blockSize #sets the x position of the player
        self.TempPlayer.rect.y = 8 * gs.blockSize #sets the y position of the player
        bph.blockPlace((6 * gs.blockSize, 6 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #places the block
        found = False #sets found to false
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True #sets found to true
        ih.addBlock(tempBlock) #adds the block to the inventory
        ih.addBlock(tempBlock) #adds the block to the inventory
        bph.blockPlace((5 * gs.blockSize, 6 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #places the block
        found = False #sets found to false
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1): #checks that the item was found
                found = True
        bph.blockPlace((8 * gs.blockSize, 8 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #places the block
        found = False #sets found to false
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1): #checks that the item was found
                found = True #sets found to true
        self.assertTrue(found) #checks that the item was found
        bph.blockPlace((800000 * gs.blockSize, 800000 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #places the block
        found = False #sets found to false
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1): #checks that the item was found
                found = True
        self.assertTrue(found) #checks that the item was found
        bph.blockPlace((5 * gs.blockSize, 6 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #places the block
        found = False
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1): #checks that the item was found
                found = True #sets found to true
        self.assertTrue(found) #checks that the item was found
        bph.blockPlace((8 * gs.blockSize, 10 * gs.blockSize), self.spriteGroup, self.TempPlayer, True) #places the block
        found = False #sets found to false
        inventory = ih.getInv() #gets the inventory
        for i in range(len(inventory)): #loops through the inventory
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1): #checks that the item was found
                found = True #sets found to true
        self.assertFalse(found) #checks that the item was not found

#tests that inventory slot class gets initlized corrected
class TestInvinventorySlots(unittest.TestCase):
    ins = InventorySlots.slot("red",10,20,30,40)

    def test_everything(self):
        self.assertEqual(self.ins.width, 30) #checks that the width is correct
        self.assertEqual(self.ins.height, 40) #checks that the height is correct
        self.assertEqual(self.ins.rect.x, 10)  #checks that the x position is correct
        self.assertEqual(self.ins.rect.y, 20) #checks that the y position is correct
        self.assertEqual(self.ins.image.get_width(), 30)  #checks that the image width is correct
        self.assertEqual(self.ins.image.get_height(), 40) #checks that the image height is correct

#test that the portal function with correct initlized
class TestPortal(unittest.TestCase):
    port = Portal.Portal(gs.blockSize,(8,7),26,textureNames[itemIDs[0]],999)

    def test_init(self):
        self.assertEqual(self.port.textureName, textureNames[itemIDs[0]]) #checks that the texture name is correct
        self.assertEqual(self.port.itemID, 26)  #checks that the item id is correct
        x = 8 - 4 * gs.blockSize #calculates the x position
        y = 7 - 8 * gs.blockSize #calculates the y position
        self.assertEqual(self.port.blockPosition, [x, y]) #checks that the block position is correct
        self.assertEqual(self.port.rect.x, 8 - 0.4 * gs.blockSize) #checks that the x position is correct
        self.assertEqual(self.port.rect.y, 7 - 1 * gs.blockSize) #checks that the y position is correct

    def test_getHardness(self):
        self.assertEqual(self.port.getHardness(), 999) #checks that the hardness is correct


# need to change tooltype and reqtooltype and drops when we used it
class TestItemNew(unittest.TestCase):
    def test_getDrop(self):
        newItems = itemNew.Item(9,"Bigblock",100,3,3,"axe","pickaxe","texture",False,"drops") #creates a new item
        self.assertEqual(newItems.getCount(), 0) #checks that the count is correct
        newItems.increase() #increases the count
        self.assertEqual(newItems.getCount(), 1) #checks that the count is correct
        newItems.decrease() #decreases the count
        self.assertEqual(newItems.getCount(), 0) #checks that the count is correct

        self.assertEqual(int, type(newItems.itemID)) #checks that the item id is correct
        self.assertEqual(str, type(newItems.itemDisplayName)) #checks that the item display name is correct
        self.assertEqual(int, type(newItems.breakTime)) #checks that the break time is correct
        self.assertEqual(int, type(newItems.blockHardness)) #checks that the block hardness is correct
        self.assertEqual(int, type(newItems.itemHardness)) #checks that the item hardness is correct
        self.assertEqual(str, type(newItems.reqToolType)) #checks that the req tool type is correct
        self.assertEqual(str, type(newItems.toolType)) #checks that the tool type is correct
        self.assertEqual(str, type(newItems.texture)) #checks that the texture is correct
        self.assertEqual(bool, type(newItems.isPlaceable)) #checks that the is placeable is correct
        self.assertEqual(str, type(newItems.drops)) #checks that the drops is correct

        self.assertEqual(newItems.getItemId(), 9) #checks that the item id is correct
        self.assertEqual(newItems.getItemName(), "Bigblock") #checks that the item name is correct
        self.assertEqual(newItems.getBreakTime(), 100) #checks that the break time is correct
        self.assertEqual(newItems.getBlockHardness(), 3) #checks that the block hardness is correct
        self.assertEqual(newItems.getItemHardness(), 3) #checks that the item hardness is correct
        self.assertEqual(newItems.getReqToolType(), "axe") #checks that the req tool type is correct
        self.assertEqual(newItems.getToolType(), "pickaxe") #checks that the tool type is correct
        self.assertEqual(newItems.getTexture(), "texture") #checks that the texture is correct
        self.assertEqual(newItems.getIsPlaceable(), False) #checks that the is placeable is correct
        self.assertEqual(newItems.getDrop(), "drops") #checks that the drops is correct

#tests relating to minecraft gym environ,emt
class testMinecraftEnv(unittest.TestCase):
    NullItem = itemArr[0]  # Item("null", -1)
    ih.invArray=np.full(40,NullItem,dtype=itemNew.Item)
    ENV = gym.make("MinePy-1", render_mode="rgb_array")
    #tests that the different settings actually change how the gym environment is generated
    def testStartModes(self):
        for i in itemArr:
            if(i.amount>0):
                i.amount=0
        ih.invArray=np.full(40,self.NullItem,dtype=itemNew.Item)
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=1)
        obs, info = self.ENV.reset(seed=6942034)
        self.assertEqual(ih.getItemCount(11), 2)  # check if the game starts with 2 wooden pickaxes
        self.assertEqual(ih.getItemCount(8), 4)  # and 4 wooden planks
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item)
        for i in itemArr:
            if(i.amount>0):
                i.amount=0
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=2)
        obs, info = self.ENV.reset(seed=6942034)
        self.assertEqual(ih.getItemCount(11), 2)  # check if the game starts with 2 wooden pickaxes
        self.assertEqual(ih.getItemCount(8), 4)  # and 4 wooden planks
        self.assertEqual(ih.getItemCount(16), 2)  # check if the game starts with 2 Stone pickaxes
        self.assertEqual(ih.getItemCount(50), 2)  # check if the game starts with a diamond
        self.assertEqual(ih.getItemCount(53), 2)  # check if the game starts with an emerald
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item)
    #tests that when the agent performs an action, the action actually takes places, specifically for movement
    def testActionSpaceMovement(self):
        
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0,seed=1212) #creates the gym environment
        
        obs, info = self.ENV.reset(seed=1212) #resets the gym environment
        prevpos = (0, 0)
        ih.fullInv=False 
        
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos # sets the previous position to the current position
            currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
            
            print(currpos," ",prevpos) #prints the current position and the previous position
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        self.ENV.step(gs.actionSpace["MOVEMENT"][1]) #moves the player forward
        
        self.assertNotEqual(currpos, self.ENV.pygame.player.getPlayerPos()) #checks that the player has moved
        self.ENV.step(gs.actionSpace["MOVEMENT"][0]) #forces the player to be on the ground
        self.ENV.step(gs.actionSpace["MOVEMENT"][0]) #forces the player to be on the ground
        self.ENV.step(gs.actionSpace["MOVEMENT"][0]) #forces the player to be on the ground
        
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        self.ENV.step(gs.actionSpace["MOVEMENT"][3]) #moves the player left
        
        self.assertNotEqual(currpos, self.ENV.pygame.player.getPlayerPos()) #checks that the player has moved
        self.ENV.step(gs.actionSpace["MOVEMENT"][0]) #forces the player to be on the ground
        
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        self.ENV.step(gs.actionSpace["MOVEMENT"][2]) #moves the player right
        
        self.assertNotEqual(currpos, self.ENV.pygame.player.getPlayerPos())

        prevpos = (0, 0)  # wait for the player to stop jumping
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos): # wait for the player to stop jumping
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos # sets the previous position to the current position
            currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
            
        self.ENV.step(gs.actionSpace["MOVEMENT"][0]) #forces the player to be on the ground
        
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        self.ENV.step(gs.actionSpace["MOVEMENT"][4]) #moves the player back
        
        self.assertNotEqual(currpos, self.ENV.pygame.player.getPlayerPos()) #checks that the player has moved

        prevpos = (0, 0)  # wait for the player to stop jumping
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        while (prevpos != currpos): # wait for the player to stop jumping
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos # sets the previous position to the current position
            currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
            
        self.ENV.step(gs.actionSpace["MOVEMENT"][0]) #forces the player to be on the ground
        
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        self.ENV.step(gs.actionSpace["MOVEMENT"][5]) #moves the player up
        
        self.assertNotEqual(currpos, self.ENV.pygame.player.getPlayerPos()) #checks that the player has moved

        prevpos = (0, 0)  # wait for the player to stop jumping
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
   #tests that when the agent performs an action, the action actually takes places, specifically for selecting a position in the hotbar
    def testActionSpaceHotBar(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=6942034)
        ih.selected = 0
        for i in range(40):
            self.ENV.step(gs.actionSpace["HOTBAR"][i])
            self.assertEqual(ih.selected, i)
    #tests that when the agent performs an action, the action actually takes places, specifically for crafting items
    def testActionSpaceCrafting(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=6942034)
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                                blockHardness[7],breakSpeed[7]) #creates a block
        ih.addBlock(tempBlock) #adds the block to the inventory
        inv = ih.getInv() #gets the inventory
        found = False #sets found to false
        for i in inv:
            if (i.itemID == 8):  # see if there are logs in the inventory
                found = True
                break
        self.assertFalse(found) #checks that there are no logs in the inventory
        self.ENV.step(gs.actionSpace["CRAFTING"][0]) #crafts a crafting table
        found = False #sets found to false
        for i in inv:
            if (i.itemID == 8):  # see if there are logs in the inventory
                found = True
                break
        self.assertTrue(found)
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item)
#tests that when the agent performs an action, the action actually takes places, specifically for breaking and placing blocks
    def testActionSpacePlaceAndBreak(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0) #creates the environment
        obs, info = self.ENV.reset(seed=1212) #resets the environment
        prevpos = (0, 0)
        #
        self.ENV.pygame.player.rect.y-=100
        currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos # sets the previous position to the current position
            currpos = self.ENV.pygame.player.getPlayerPos() #gets the current position of the player
            #
        ih.clearInv()
        tempBlock = block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                                blockHardness[7],breakSpeed[7]) #creates a block
        for i in range(5):
            ih.addBlock(tempBlock) #adds the block to the inventory
        self.assertEqual(ih.getItemCount(7), 5)  # check that there are 10 logs in the inventory
        #
        inv = ih.getInv()
        for i in range(len(inv)): #loops through the inventory
            if (inv[i].itemID == 7): #checks if the item is a log
                ih.selected = i #sets the selected item to the log
                break #breaks the loop
        count = 5 #sets the count to 5
        for i in range(5):
            playerPos=[self.ENV.pygame.player.getPlayerPos()[0],self.ENV.pygame.player.getPlayerPos()[1]]
            offset = [[-1,-1],[0,-1],[1,-1],  # offsets of player positions, top row is above player
                       [-1,0],[-1,1],[1,0],[1,1],  # left down, left up, right down, right up
                       [-1,2],[0,2],[1,2]]
            playerPos[0] += offset[i][0] * gs.blockSize # adds the offset to the player position
            playerPos[1] += offset[i][1] * gs.blockSize     # adds the offset to the player position                          
            bPos = bph.getBlockFromPos(playerPos, self.ENV.pygame.worldBlocks) #gets the block from the position
            if(bPos.itemID==-1): #checks if the block is air
                count -= 1
                self.ENV.step(gs.actionSpace["WORLD"][10 + i]) #places a block
                self.assertEqual(ih.getItemCount(7), count) # check that there are 10 logs in the inventory
            
        count = 0
        for i in range(5):
            count += 1
            self.ENV.step(gs.actionSpace["WORLD"][i])  # break blocks around the player
            self.assertEqual(ih.getItemCount(7), count)  # see if it got readded to the inventory
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item)
    #tests that recieving rewards work
    def testEvaluateGeneralRewards(self): #tests that recieving rewards work
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212) #resets the environment

        # test general movement reward
        for i in range(5):
            Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["MOVEMENT"][i])
            self.assertEqual(reward, 0.01)

        # test general hotbar
        for i in range(40):
            Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][i])
            self.assertEqual(reward, 0.01)
    #tests that when performing the actions required for stage 1 of the rewards, the correct rewards are given
    def testEvaluateStage1(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
        stage1Blocks = [

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),6,textureNames["Oak Leaves"],
                    blockHardness[6],breakSpeed[6]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),1,textureNames["Dirt Block"],
                    blockHardness[1],breakSpeed[1]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),0,textureNames["Grass Block"],
                    blockHardness[0],breakSpeed[0])]

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        # stage 1 breaking and placing
        k = 0
        for i in (stage1Blocks):
            ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
            ih.addBlock(i)
            self.ENV.step(gs.actionSpace["HOTBAR"][0])
            Obs, reward, done, boolo, infoDict =self.ENV.step(gs.actionSpace["WORLD"][11])
            if(k == 1):
                self.assertEqual(reward, -5)
            else:
                self.assertEqual(reward, 0.01)
            Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
            stages = rewardsHandler.populateStages()
            currStage = stages["Stage" + "1"]
            self.assertEqual(reward, currStage.getAcquisitionRewards()[k])
            k+=1
        
        # passing stage 1 by having 2 or more wooden planks in inv
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        for i in range(2):
            ih.addBlock(stage1Blocks[1])
        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][0])
        self.assertEqual(reward, 10)
    #tests that when performing the actions required for stage 2 of the rewards, the correct rewards are given
    def testEvaluateStage2Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
        stage2Blocks = [

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11])]
        
        for i in range(2): # get to stage 2
            ih.addBlock(stage2Blocks[1])

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()

        for i in range(8): # get to stage 3
            ih.addBlock(stage2Blocks[0])
        
        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 20) # complete state 2 rewards
    #tests that when performing the actions required for stage 3 of the rewards, the correct rewards are given
    def testEvaluateStage3Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
        stage3Blocks = [

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11])]


        for i in range(2): # get to stage 2
            ih.addBlock(stage3Blocks[1])
        for i in range(8): # get to stage 3
            ih.addBlock(stage3Blocks[0])

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        ih.addBlock(stage3Blocks[2]) # get to stage 4
        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 30) # complete state 3 rewards
#tests that when performing the actions required for stage 4 of the rewards, the correct rewards are given
    def testEvaluateStage4Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)

        # log ,plank, pickaxe, stone, leaves, dirt, grass
        stage4Blocks = [
        
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"],
                    blockHardness[2],breakSpeed[2]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),6,textureNames["Oak Leaves"],
                    blockHardness[6],breakSpeed[6]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),1,textureNames["Dirt Block"],
                    blockHardness[1],breakSpeed[1]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),0,textureNames["Grass Block"],
                    blockHardness[0],breakSpeed[0])]

        for i in range(2): # get to stage 2
            ih.addBlock(stage4Blocks[0])
        for i in range(8): # get to stage 3
            ih.addBlock(stage4Blocks[1])
        ih.addBlock(stage4Blocks[2]) # get to stage 4
        
        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        # log ,plank, pickaxe, stone, leaves, dirt, grass
        rewardsWithPickaxe = [20, 50, -1, 50, 12, 11, 13]

        k = 0
        for i in (stage4Blocks):
            if(k != 2):
                ih.addBlock(i)
                self.ENV.step(gs.actionSpace["HOTBAR"][k])
                self.ENV.step(gs.actionSpace["WORLD"][11])
                self.ENV.step(gs.actionSpace["HOTBAR"][2]) # select pickaxe
                Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
                self.assertEqual(reward, rewardsWithPickaxe[k])
            k+=1

        k = 0
        for i in (stage4Blocks):
            if(k != 2):
                ih.addBlock(i)
                self.ENV.step(gs.actionSpace["HOTBAR"][k])
                self.ENV.step(gs.actionSpace["WORLD"][11])
                if(k == 3):
                    self.ENV.step(gs.actionSpace["HOTBAR"][2]) # select pickaxe
                    Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
                    self.assertEqual(reward, rewardsWithPickaxe[k])
                else:
                    Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
                    self.assertEqual(reward, rewardsWithPickaxe[k] - 20)
            k+=1

        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        for i in range(3):
            ih.addBlock(stage4Blocks[3])
            ih.addBlock(stage4Blocks[1])
        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][0])
        self.assertEqual(reward, 40)
        
    #tests that when performing the actions required for stage 5 of the rewards, the correct rewards are given
    def testEvaluateStage5Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        stage5Blocks = [
        
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"],
                    blockHardness[2],breakSpeed[2]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),16,textureNames["Stone Pickaxe"],
                    blockHardness[16],breakSpeed[16])]


        for i in range(2): # get to stage 2
            ih.addBlock(stage5Blocks[0])
        for i in range(8): # get to stage 3
            ih.addBlock(stage5Blocks[1])
        ih.addBlock(stage5Blocks[2]) # get to stage 4
        for i in range(3):
            ih.addBlock(stage5Blocks[3]) #get to stage 5

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        ih.addBlock(stage5Blocks[4]) # get to stage 6
        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 50) # complete state 5 rewards
    #tests that when performing the actions required for stage 6 of the rewards, the correct rewards are given
    def testEvaluateStage6Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
         # logs, planks, woodenpickaxxe, stone, stonepickaxe, leaves, dirt, grass, gold, diamond, emerald
        stage6Blocks = [
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11]),
            
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"],
                    blockHardness[2],breakSpeed[2]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),16,textureNames["Stone Pickaxe"],
                    blockHardness[16],breakSpeed[16]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),6,textureNames["Oak Leaves"],
                    blockHardness[6],breakSpeed[6]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),1,textureNames["Dirt Block"],
                    blockHardness[1],breakSpeed[1]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),0,textureNames["Grass Block"],
                    blockHardness[0],breakSpeed[0]),
                            
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),46,textureNames["Gold Ore"],
                    blockHardness[46],breakSpeed[46]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),49,textureNames["Diamond Ore"],
                    blockHardness[49],breakSpeed[49]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),78,textureNames["Emerald Ore"],
                    blockHardness[78],breakSpeed[78])]


        for i in range(2): # get to stage 2
            ih.addBlock(stage6Blocks[0])
        for i in range(8): # get to stage 3
            ih.addBlock(stage6Blocks[1])
        ih.addBlock(stage6Blocks[2]) # get to stage 4
        for i in range(3):
            ih.addBlock(stage6Blocks[3]) #get to stage 5
        ih.addBlock(stage6Blocks[4]) # get to stage 6

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()

        #logs, planks, woodenpickaxxe, stone, stonepickaxe, leaves, dirt, grass, gold, diamond, emerald
        stonePickRewards=[50, 80, -1, 80, -1, 42, 41, 43, 100, 100, 100]
        k = 0
        for i in (stage6Blocks): # break with stone pickaxe only
            if(k != 2 and k != 4):
                ih.addBlock(i)
                self.ENV.step(gs.actionSpace["HOTBAR"][k])
                self.ENV.step(gs.actionSpace["WORLD"][11])
                self.ENV.step(gs.actionSpace["HOTBAR"][4]) # select stone pickaxe
                Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
                self.assertEqual(reward, stonePickRewards[k])
            k+=1

        woodenPickRewards = [-30, 0, -1, 0, -1, -38, -39, -37, 100, 100, 100]
        k = 0
        for i in (stage6Blocks): # break with wooden pickaxe
            if(k != 2 and k != 4):
                ih.addBlock(i)
                self.ENV.step(gs.actionSpace["HOTBAR"][k])
                self.ENV.step(gs.actionSpace["WORLD"][11])
                if(k == 8 or k == 9 or k == 10):
                    self.ENV.step(gs.actionSpace["HOTBAR"][4]) # select stone pickaxe
                    Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
                    self.assertEqual(reward, woodenPickRewards[k])
                else:
                    self.ENV.step(gs.actionSpace["HOTBAR"][2]) # select wooden pickaxe
                    Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["WORLD"][1])
                    self.assertEqual(reward, woodenPickRewards[k])
            k+=1

        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        for i in range(36):
                ih.addBlock(stage6Blocks[8])
                ih.addBlock(stage6Blocks[9])
        ih.addBlock(stage6Blocks[10])
        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 60) # complete state 6 rewards
    #tests that when performing the actions required for stage 7 of the rewards, the correct rewards are given    
    def testEvaluateStage7Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
        stage7Blocks = [
        
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"],
                    blockHardness[2],breakSpeed[2]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),16,textureNames["Stone Pickaxe"],
                    blockHardness[16],breakSpeed[16]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),46,textureNames["Gold Ore"],
                    blockHardness[46],breakSpeed[46]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),49,textureNames["Diamond Ore"],
                    blockHardness[49],breakSpeed[49]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),78,textureNames["Emerald Ore"],
                    blockHardness[78],breakSpeed[78]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),50,textureNames["Gold Ingot"],
                    blockHardness[50],breakSpeed[50]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),47,textureNames["Diamond"],
                    blockHardness[47],breakSpeed[47]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),53,textureNames["Emerald"],
                    blockHardness[53],breakSpeed[53])]



        for i in range(2): # get to stage 2
            ih.addBlock(stage7Blocks[0])
        for i in range(8): # get to stage 3
            ih.addBlock(stage7Blocks[1])
        ih.addBlock(stage7Blocks[2]) # get to stage 4
        for i in range(3):
            ih.addBlock(stage7Blocks[3]) #get to stage 5
        ih.addBlock(stage7Blocks[4]) # get to stage 6
        
        for i in range(36):
            ih.addBlock(stage7Blocks[5])
            ih.addBlock(stage7Blocks[6])
        ih.addBlock(stage7Blocks[7]) # get to stage 7

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        for i in range(36):
            ih.addBlock(stage7Blocks[8])
            ih.addBlock(stage7Blocks[9])
        ih.addBlock(stage7Blocks[10]) # get to stage 8

        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 70) # complete state 7 rewards
    #tests that when performing the actions required for stage 8 of the rewards, the correct rewards are given
    def testEvaluateStage8Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
        stage8Blocks = [
        
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"],
                    blockHardness[2],breakSpeed[2]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),16,textureNames["Stone Pickaxe"],
                    blockHardness[16],breakSpeed[16]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),46,textureNames["Gold Ore"],
                    blockHardness[46],breakSpeed[46]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),49,textureNames["Diamond Ore"],
                    blockHardness[49],breakSpeed[49]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),78,textureNames["Emerald Ore"],
                    blockHardness[78],breakSpeed[78]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),50,textureNames["Gold Ingot"],
                    blockHardness[50],breakSpeed[50]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),47,textureNames["Diamond"],
                    blockHardness[47],breakSpeed[47]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),53,textureNames["Emerald"],
                    blockHardness[53],breakSpeed[53]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),64,textureNames["Gold Block"],
                    blockHardness[64],breakSpeed[64]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),67,textureNames["Diamond Block"],
                    blockHardness[67],breakSpeed[67])]



        for i in range(2): # get to stage 2
            ih.addBlock(stage8Blocks[0])
        for i in range(8): # get to stage 3
            ih.addBlock(stage8Blocks[1])
        ih.addBlock(stage8Blocks[2]) # get to stage 4
        for i in range(3):
            ih.addBlock(stage8Blocks[3]) #get to stage 5
        ih.addBlock(stage8Blocks[4]) # get to stage 6
        
        for i in range(36):
            ih.addBlock(stage8Blocks[5])
            ih.addBlock(stage8Blocks[6])
        ih.addBlock(stage8Blocks[7]) # get to stage 7

        for i in range(36):
            ih.addBlock(stage8Blocks[8])
            ih.addBlock(stage8Blocks[9])
        ih.addBlock(stage8Blocks[10]) # get to stage 8

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        for i in range(36):
            ih.addBlock(stage8Blocks[11])
            ih.addBlock(stage8Blocks[12]) # get to stage 9

        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 80) # complete state 8 rewards
#tests that when performing the actions required for stage 9 of the rewards, the correct rewards are given
    def testEvaluateStage9Progess(self):
        self.ENV = gym.make("MinePy-1", render_mode="rgb_array",easyStart=0)
        obs, info = self.ENV.reset(seed=1212)
        
        stage9Blocks = [
        
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),7,textureNames["Oak Log"],
                    blockHardness[7],breakSpeed[7]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),8,textureNames["Oak Planks"],
                    blockHardness[8],breakSpeed[8]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),11,textureNames["Wooden Pickaxe"],
                    blockHardness[11],breakSpeed[11]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),2,textureNames["Stone Block"],
                    blockHardness[2],breakSpeed[2]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),16,textureNames["Stone Pickaxe"],
                    blockHardness[16],breakSpeed[16]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),46,textureNames["Gold Ore"],
                    blockHardness[46],breakSpeed[46]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),49,textureNames["Diamond Ore"],
                    blockHardness[49],breakSpeed[49]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),78,textureNames["Emerald Ore"],
                    blockHardness[78],breakSpeed[78]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),50,textureNames["Gold Ingot"],
                    blockHardness[50],breakSpeed[50]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),47,textureNames["Diamond"],
                    blockHardness[47],breakSpeed[47]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),53,textureNames["Emerald"],
                    blockHardness[53],breakSpeed[53]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),64,textureNames["Gold Block"],
                    blockHardness[64],breakSpeed[64]),

        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),67,textureNames["Diamond Block"],
                    blockHardness[67],breakSpeed[67]),
                                
        block.Block(gs.blockSize,(9 * gs.blockSize,9 * gs.blockSize),83,textureNames["End Game Block"],
                    blockHardness[83],breakSpeed[83])]



        for i in range(2): # get to stage 2
            ih.addBlock(stage9Blocks[0])
        for i in range(8): # get to stage 3
            ih.addBlock(stage9Blocks[1])
        ih.addBlock(stage9Blocks[2]) # get to stage 4
        for i in range(3):
            ih.addBlock(stage9Blocks[3]) #get to stage 5
        ih.addBlock(stage9Blocks[4]) # get to stage 6
        
        for i in range(36):
            ih.addBlock(stage9Blocks[5])
            ih.addBlock(stage9Blocks[6])
        ih.addBlock(stage9Blocks[7]) # get to stage 7

        for i in range(36):
            ih.addBlock(stage9Blocks[8])
            ih.addBlock(stage9Blocks[9])
        ih.addBlock(stage9Blocks[10]) # get to stage 8

        for i in range(36):
            ih.addBlock(stage9Blocks[11])
            ih.addBlock(stage9Blocks[12]) # get to stage 9

        prevpos = (0, -100)
        
        currpos = self.ENV.pygame.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.step(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.pygame.player.getPlayerPos()
        
        ih.invArray = np.full(40,self.NullItem,dtype=itemNew.Item) # clear the inv
        ih.addBlock(stage9Blocks[13]) # complete game

        Obs, reward, done, boolo, infoDict = self.ENV.step(gs.actionSpace["HOTBAR"][1])
        self.assertEqual(reward, 1000) # complete game rewards

unittest.main()

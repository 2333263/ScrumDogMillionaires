import unittest
from numpy import ndarray
import Camera
# import item
import gameSettings as gs
import block
import pygame
import CraftButtonHandler
import TextHandler
import recipeHandler
import playerHandler as ph
import CraftingMenu
import inventoryHandler as ih
import breakPlaceHandler as bph
import InventorySlots
import ChunkGenerator as CG
import ChunkHandler as CH
import Portal
import itemNew
# from itemHandler import populateDictionaries
import itemHandler
import numpy as np
from gym_MC.envs import minecraftEnv as MCENV

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
class TestItem(unittest.TestCase):
    tempItem = itemArr[1]  # Item("Grass", 0)
    tempItem1 = itemArr[2]  # Item("Dirt", 0, 20)]
    tempItem1.itemHardness=20

    def test_itemID(self):
        self.assertIsInstance(self.tempItem.itemID, int)
        self.assertGreaterEqual(self.tempItem.itemID, 0)
        self.assertLessEqual(self.tempItem.itemID, len(itemIDs) + 1)
        self.assertEqual(self.tempItem.getItemId(), self.tempItem.itemID)
        self.assertIsInstance(self.tempItem1.itemID, int)
        self.assertGreaterEqual(self.tempItem1.itemID, 0)
        self.assertLessEqual(self.tempItem1.itemID, len(itemIDs) + 1)
        self.assertEqual(self.tempItem1.getItemId(), self.tempItem1.itemID)

    def test_amount(self):
        self.assertIsInstance(self.tempItem.amount, int)
        self.assertGreaterEqual(self.tempItem.amount, 0)
        self.assertIsInstance(self.tempItem1.amount, int)
        self.assertGreaterEqual(self.tempItem1.amount, 0)
        oldCount = self.tempItem.amount
        self.tempItem.increase()
        self.assertGreaterEqual(self.tempItem.amount, oldCount)
        self.tempItem.decrease()
        self.assertEqual(self.tempItem.amount, oldCount)
        self.assertEqual(self.tempItem.amount, self.tempItem.getCount())

    def test_name(self):
        self.assertIsInstance(self.tempItem.itemDisplayName, str)
        self.assertEqual(self.tempItem.getItemName(), "Grass Block")
        self.assertIsInstance(self.tempItem1.itemDisplayName, str)
        self.assertEqual(self.tempItem1.getItemName(), "Dirt Block")

    def test_Hardness(self):
        self.assertEqual(self.tempItem.getItemHardness(), 0)
        self.assertEqual(self.tempItem1.getItemHardness(), 20)


class TestBlock(unittest.TestCase):
    tempBlock = block.Block(gs.blockSize, (0, 0), 0, textureNames[itemIDs[0]], 0, breakSpeed[0])

    def test_itemIDs(self):
        self.assertIsInstance(self.tempBlock.itemID, int)
        self.assertGreaterEqual(self.tempBlock.itemID, 0)
        self.assertLessEqual(self.tempBlock.itemID, len(itemIDs) + 1)

    def test_positions(self):
        self.assertGreaterEqual(self.tempBlock.blockPosition[0], 0)
        self.assertGreaterEqual(self.tempBlock.blockPosition[1], 0)

        self.assertLessEqual(self.tempBlock.blockPosition[0], gs.width)
        self.assertLessEqual(self.tempBlock.blockPosition[1], gs.height)

    def test_texture(self):
        self.assertIsInstance(self.tempBlock.textureName, str)
        self.assertIsInstance(self.tempBlock.rect, pygame.rect.Rect)
        # Add check for texture object

    def test_hardness(self):
        self.assertEqual(self.tempBlock.getHardness(), 0)


class TestCraftingButton(unittest.TestCase):
    tempButton = CraftButtonHandler.Button(0, (0, 0), 50, 50)
    pygame.init()

    def test_itemIDs(self):
        self.assertIsInstance(self.tempButton.itemID, int)
        self.assertGreaterEqual(self.tempButton.itemID, 0)
        self.assertLessEqual(self.tempButton.itemID, len(itemIDs) + 1)

    def test_positions(self):
        self.assertGreaterEqual(self.tempButton.pos[0], 0)
        self.assertGreaterEqual(self.tempButton.pos[1], 0)

        self.assertLessEqual(self.tempButton.pos[0], gs.width)
        self.assertLessEqual(self.tempButton.pos[1], gs.height)

    def test_rectangle(self):
        self.assertIsInstance(self.tempButton.rect, pygame.rect.Rect)


class TestTextHandler(unittest.TestCase):
    testText = TextHandler.Text("TestCase", 12, "red", (0, 0))

    def test_text(self):
        self.assertIsInstance(self.testText.words, str)
        self.assertIsInstance(self.testText.my_font, pygame.font.Font)
        self.assertIsInstance(self.testText.rect, pygame.rect.Rect)

    def test_positions(self):
        self.assertGreaterEqual(self.testText.pos[0], 0)
        self.assertGreaterEqual(self.testText.pos[1], 0)

        self.assertLessEqual(self.testText.pos[0], gs.width)
        self.assertLessEqual(self.testText.pos[1], gs.height)


class TestRecipeHandler(unittest.TestCase):
    tempHandler = recipeHandler.RecipeHandler()

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


class TestPlayer(unittest.TestCase):
    TempPlayer = ph.Player((8 * gs.blockSize, 8 * gs.blockSize), 24)

    def test_innit(self):
        self.assertEqual(self.TempPlayer.rect.x, 8 * gs.blockSize)
        self.assertEqual(self.TempPlayer.rect.y, 8 * gs.blockSize)
        self.assertTrue(type(self.TempPlayer) is ph.Player)

    def test_pos(self):
        self.assertEqual(self.TempPlayer.getPlayerPos(), (8 * gs.blockSize, 8 * gs.blockSize))

    # this is a comment
    def test_MoveX(self):
        # empty={}
        # self.TempPlayer.MoveOnX(empty)
        # self.assertNotEqual(len(self.TempPlayer.keys),0)
        self.simulatedKeys = {
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_a: False,
            pygame.K_d: False
        }
        self.simulatedKeys[pygame.K_LEFT] = True
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, -2)
        self.simulatedKeys[pygame.K_LEFT] = False
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, 0)

        self.simulatedKeys[pygame.K_a] = True
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, -2)
        self.simulatedKeys[pygame.K_a] = False
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, 0)

        self.simulatedKeys[pygame.K_RIGHT] = True
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, 2)
        self.simulatedKeys[pygame.K_RIGHT] = False
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, 0)

        self.simulatedKeys[pygame.K_d] = True
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, 2)
        self.simulatedKeys[pygame.K_d] = False
        self.TempPlayer.MoveOnX(self.simulatedKeys)
        self.assertEqual(self.TempPlayer.direction.x, 0)

    def test_gravity(self):
        self.TempPlayer.useGravity()
        self.assertEqual(self.TempPlayer.direction.y, self.TempPlayer.gravity)
        self.TempPlayer.direction.y = 0

    def test_jump(self):
        # jumped is false by default in case we spawn the player above the world
        self.assertEqual(self.TempPlayer.jumped, False)
        self.TempPlayer.jump()
        self.assertEqual(self.TempPlayer.jumped, True)
        self.assertEqual(self.TempPlayer.direction.y, -8.5)
        self.TempPlayer.jumped = False

    def test_jumping_acceleration(self):
        self.TempPlayer.jumpArc()
        # check if player is jumped get set to false when direction.y==0
        self.assertEqual(self.TempPlayer.jumped, False)
        self.TempPlayer.direction.y = -5
        # testing if the grabity acceleration changes
        self.TempPlayer.jumpArc()
        self.assertEqual(self.TempPlayer.direction.y, -5 + self.TempPlayer.gravity / 5)
        self.TempPlayer.direction.y = 0

    # NEED TO BE REWRITTEN
    def test_update(self):
        tempBlock = block.Block(gs.blockSize, (8, 7), 0, textureNames[itemIDs[0]], 0, breakSpeed[0])
        tempGroup = pygame.sprite.Group()
        tempGroup.add(tempBlock)
        self.TempPlayer.jumped = True
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.jumped, False)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.y, 4.0)
        for x in tempGroup:
            x.blockPosition = (8 * gs.blockSize, 10 * gs.blockSize)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.y, 4.0)
        self.TempPlayer.direction.x = -1
        for x in tempGroup:
            x.blockPosition = (7 * gs.blockSize, 8 * gs.blockSize)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.x, -1.0)
        self.TempPlayer.direction.x = -1
        for x in tempGroup:
            x.blockPosition = (7 * gs.blockSize, 9 * gs.blockSize)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.x, -1.0)
        self.TempPlayer.direction.x = 1
        for x in tempGroup:
            x.blockPosition = (9 * gs.blockSize, 8 * gs.blockSize)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.x, 1.0)
        self.TempPlayer.direction.x = 1
        for x in tempGroup:
            x.blockPosition = (9 * gs.blockSize, 9 * gs.blockSize)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.x, 1.0)
        self.TempPlayer.jumped = True
        for x in tempGroup:
            x.blockPosition = (8 * gs.blockSize, 8 * gs.blockSize)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.direction.y, 4.8)
        self.TempPlayer.direction.x = 1
        self.TempPlayer.direction.y = 1
        tempPosX = self.TempPlayer.rect.x
        tempPosY = self.TempPlayer.rect.y
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(self.TempPlayer.rect.y, tempPosY + 1)
        self.assertEqual(self.TempPlayer.rect.x, tempPosX + 1)
        self.TempPlayer.rect.x = tempPosX
        self.TempPlayer.rect.y = tempPosY
        self.TempPlayer.update(2, tempGroup)
        self.assertEqual(self.TempPlayer.rect.y, tempPosY + 5)
        self.assertEqual(self.TempPlayer.rect.x, tempPosX + 2)
        tempBlock = block.Block(gs.blockSize, (8 * gs.blockSize, 7 * gs.blockSize), 0, textureNames[itemIDs[0]],
                                0, breakSpeed[0])
        tempGroup.add(tempBlock)
        self.TempPlayer.rect.x = 8 * gs.blockSize - 1
        self.TempPlayer.rect.y = 7 * gs.blockSize
        self.TempPlayer.direction.x = 1

        self.TempPlayer.update(1, tempGroup)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(8 * gs.blockSize - 1, self.TempPlayer.rect.x)
        self.TempPlayer.rect.x = 8 * gs.blockSize + 1
        self.TempPlayer.rect.y = 7 * gs.blockSize
        self.TempPlayer.direction.x = -1
        self.TempPlayer.update(1, tempGroup)
        self.TempPlayer.update(0, tempGroup)
        self.assertEqual(8 * gs.blockSize + 1, self.TempPlayer.rect.x)
        self.TempPlayer.jumped = True
        self.TempPlayer.rect.x = 8 * gs.blockSize
        self.TempPlayer.rect.y = 7 * gs.blockSize
        self.TempPlayer.direction.y = -3
        self.TempPlayer.update(1, tempGroup)
        self.assertEqual(tempBlock.rect.bottom, self.TempPlayer.rect.top)
        self.assertFalse(self.TempPlayer.jumped)
        self.TempPlayer.rect.x = 8 * gs.blockSize
        self.TempPlayer.rect.y = 7 * gs.blockSize - 1
        self.TempPlayer.direction.y = 3

        self.TempPlayer.update(1, tempGroup)
        self.assertEqual(tempBlock.rect.top, self.TempPlayer.rect.bottom)

    def test_StopOnX(self):
        self.TempPlayer.stopMoveOnX()
        self.assertEqual(self.TempPlayer.direction.x, 0)

    def test_willcolide(self):
        tempBlock = block.Block(gs.blockSize, (8, 7), 0, textureNames[itemIDs[0]], 0, breakSpeed[0])
        tempGroup = pygame.sprite.Group()
        tempGroup.add(tempBlock)

        self.TempPlayer.rect.x = 8
        self.TempPlayer.rect.y = 7
        self.assertTrue(self.TempPlayer.willcollide(tempBlock))
        self.TempPlayer.rect.x = 22 * gs.blockSize
        self.TempPlayer.rect.y = 22 * gs.blockSize
        self.assertFalse(self.TempPlayer.willcollide(tempBlock))


class TestCraftingMenu(unittest.TestCase):
    screen = pygame.display
    crafter = CraftingMenu.Crafting(screen)

    def test_innit(self):  # I had to call it AAinit so it would run before the other test cases
        self.crafter.initGroup()
        self.assertIsInstance(CraftingMenu.slots, pygame.sprite.Group)
        self.assertEqual(len(CraftingMenu.slots), 10)

    def test_relativeSize(self):
        self.assertTrue(self.crafter.relativeSize >= 0 and self.crafter.relativeSize <= gs.blockSize * 3)

    def test_allItems(self):
        self.assertIsInstance(list(), type(self.crafter.allItems))

    def test_emptyTable(self):
        NullItem = itemArr[0]  # Null item, id -1
        self.crafter.emptyTable()
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.crafter.craftArray[i][j].itemID, -1)
        self.assertEqual(self.crafter.canCraft, False)
        self.assertEqual(self.crafter.craftID, -1)

    def test_checkCanCraft(self):
        self.crafter.emptyTable()
        self.crafter.checkCanCraft()
        self.assertEqual(self.crafter.canCraft, False)
        self.assertEqual(self.crafter.craftID, -1)
        self.crafter.craftArray[1][1] = itemArr[8]  # Item("Logs", 7)
        self.crafter.checkCanCraft()
        self.assertEqual(self.crafter.canCraft, True)
        self.assertEqual(self.crafter.craftID, 8)

    def test_doCraft(self):
        NullItem = itemArr[0]  # Null item, id -1
        self.crafter.emptyTable()
        self.crafter.doCraft()
        self.assertEqual(self.crafter.canCraft, False)
        self.assertEqual(self.crafter.craftID, -1)
        self.crafter.craftArray[1][1] = itemArr[8]  # Item("Logs", 7)
        ih.invArray = np.full(40, NullItem, dtype=itemNew.Item)
        curr = ih.getItemCount(8)
        self.crafter.doCraft()
        self.assertEqual(ih.getItemCount(8), curr + 4)
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.crafter.craftArray[i][j].itemID, -1)
        self.assertEqual(self.crafter.canCraft, False)
        self.assertEqual(self.crafter.craftID, -1)
        self.crafter.craftArray[1][1] = itemArr[47]  # Item("Gold Ore", 46)
        curr = ih.getItemCount(47)
        self.crafter.doCraft()
        self.assertEqual(ih.getItemCount(47), curr + 1)
        ih.invArray = np.full(40, NullItem, dtype=itemNew.Item)
        for i in itemArr:
            if(i.amount>0):
                i.amount=0
    def testCraftSpec(self):
        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 7, textureNames["Oak Log"],
                                blockHardness[7], breakSpeed[7])
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
    

class TestGameSettings(unittest.TestCase):
    def test_properties(self):
        self.assertIsInstance(gs.blockSize, int)
        self.assertGreaterEqual(gs.blockSize, 1)

        self.assertIsInstance(gs.playerRange, int)
        self.assertGreaterEqual(gs.playerRange, 1)

        self.assertIsInstance(gs.width, int)
        self.assertGreaterEqual(gs.width, 1)
        self.assertIsInstance(gs.height, int)
        self.assertGreaterEqual(gs.height, 1)

        self.assertIsInstance(gs.drawCrafting, bool)

        self.assertIsInstance(gs.craftingTablePos[0], int)
        self.assertGreaterEqual(gs.craftingTablePos[0], 1)
        self.assertIsInstance(gs.craftingTablePos[1], int)
        self.assertGreaterEqual(gs.craftingTablePos[1], 1)

        self.assertIsInstance(itemIDs, dict)
        self.assertIsInstance(craftingIDs, dict)
        self.assertIsInstance(converterIDs, dict)
        self.assertIsInstance(textureNames, dict)

        self.assertIsInstance(immovableBlocks, list)
        self.assertIsInstance(clickableBlocks, list)


class TestInv(unittest.TestCase):
    def testAAInit(self):  # I had to call it AAinit so it would run before the other test cases
        inventory = ih.getInv()
        empty = True
        for i in inventory:
            if (i.getItemId() != -1):
                empty = False
        self.assertTrue(empty)
        ih.initGroup()
        self.assertIsInstance(ih.slots, pygame.sprite.Group)
        self.assertEqual(len(ih.slots), 40)
        ih.selected = 0
        self.assertEqual(ih.getSelected().getItemId(), 5)

    def testAddBlockandRemove(self):
        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 7, textureNames["Oak Log"],
                                blockHardness[7], breakSpeed[7])
        ih.addBlock(tempBlock)
        found = False
        foundPos = 0
        inv = ih.getInv()
        for i in range(len(inv)):
            if (inv[i].getItemId() == 7):
                foundPos = i
                found = True
        self.assertTrue(found)
        self.assertEqual(inv[foundPos].getCount(), 1)
        ih.addBlock(tempBlock)
        self.assertEqual(inv[foundPos].getCount(), 2)
        ih.selected = foundPos
        ih.decrease()
        self.assertEqual(inv[foundPos].getCount(), 1)
        ih.decrease()
        self.assertEqual(inv[foundPos].getItemId(), -1)

    def testDecSpec(self):
        inv = ih.getInv()
        self.assertEqual(inv[0].getItemId(), 5)  # crafting table is in position 0
        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 7, textureNames["Oak Log"],
                                blockHardness[7], breakSpeed[7])
        ih.addBlock(tempBlock)  # should be in position 1
        inv = ih.getInv()
        self.assertEqual(inv[1].getItemId(), 7)
        ih.selected = 0
        ih.decreaseSpec(7)
        self.assertEqual(inv[1].getItemId(), -1)

    def testAddItem(self):
        found = False
        inv = ih.getInv()
        for i in inv:
            if (i.getItemId() == 11):
                found = True
        self.assertFalse(found)
        tempItem = itemArr[12]  # Item("Wooden Pickaxe", 11)
        ih.addItem(tempItem)
        ih.addItem(tempItem)
        found = False
        inv = ih.getInv()
        for i in inv:
            if (i.getItemId() == 11):
                found = True
        self.assertTrue(found)
        foundpos = 0
        inv = ih.getInv()
        for i in range(len(inv)):
            if (inv[i].getItemId() == 11):
                foundpos = i
        self.assertEqual(inv[foundpos].getCount(), 2)
        ih.decreaseSpec(11)
        ih.decreaseSpec(11)

    def testSelection(self):
        ih.selected = 0
        ih.selectNext()
        self.assertEqual(ih.selected, 1)
        ih.selected = 9
        ih.selectNext()
        self.assertEqual(ih.selected, 0)
        ih.selectPrevious()
        self.assertEqual(ih.selected, 9)
        ih.selectPrevious()
        self.assertEqual(ih.selected, 8)
        ih.selectInventory(7)
        self.assertEqual(ih.selected, 7)
        ih.selected = 0

    def testGetitemCount(self):
        self.assertEqual(ih.getItemCount(5), 1)
        self.assertEqual(ih.getItemCount(14), 0)

    def testClick(self):
        ih.fullInv = False
        ih.selected = 0
        self.assertEqual(ih.selected, 0)
        ih.onClick((12 * ih.relative + 3 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.selected, 3)
        ih.fullInv = True
        self.assertEqual(ih.getClicked(), -1)
        ih.onClick((12 * ih.relative + 0 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.clicked, 0)
        ih.onClick((12 * ih.relative + 3 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.getClicked(), -1)
        foundPos = 0
        inv = ih.getInv()
        for i in range(len(inv)):
            if (inv[i].getItemId() == 5):
                foundPos = i
        self.assertEqual(foundPos, 3)
        ih.onClick((12 * ih.relative + 0 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.clicked, 0)
        ih.onClick((12 * ih.relative + 3 * 85 * ih.relative, 30 * ih.relative + 15 * ih.relative))
        self.assertEqual(ih.clicked, -1)
        ih.setClicked()
        self.assertEqual(ih.getClicked(), -1)


class TestCamera(unittest.TestCase):
    TempPlayer = ph.Player((8 * gs.blockSize, 8 * gs.blockSize), 24)
    Cam = Camera.Camera(TempPlayer)
    # pygame.display.set_mode((1280, 720))
    screen = pygame.Surface((gs.blockSize, gs.blockSize))
    tempBlock = block.Block(gs.blockSize, (8, 7), 0, textureNames[itemIDs[0]], 0, breakSpeed[0])
    tempBlock2 = block.Block(gs.blockSize, (20, 7), 1, textureNames[itemIDs[1]], 0, breakSpeed[1])
    tempBlock3 = block.Block(gs.blockSize, (29, 7), 2, textureNames[itemIDs[1]], 0, breakSpeed[2])
    tempBlock4 = block.Block(gs.blockSize, (50, 7), 3, textureNames[itemIDs[1]], 0, breakSpeed[3])

    def test_Offset(self):
        self.Cam.scroll()
        # self.assertEqual(self.Cam.offset,pygame.math.Vector2(-558,-176))
        self.assertEqual(self.Cam.getOffsets(), self.Cam.offset)

    def test_Collide(self):
        self.assertFalse(self.Cam.isColideable(self.tempBlock))
        self.tempBlock.rect.x = 8 * gs.blockSize
        self.tempBlock.rect.y = 8 * gs.blockSize
        self.assertTrue(self.Cam.isColideable(self.tempBlock))

    def test_onScreen(self):
        self.assertTrue(self.Cam.isOnScreen(self.tempBlock))
        self.tempBlock.rect.x = 1000
        self.tempBlock.rect.y = 1000
        # self.assertFalse(self.Cam.isOnScreen(self.tempBlock))

    def test_draw(self):
        self.tempBlock.rect.x = 8 * gs.blockSize
        self.tempBlock.rect.y = 8 * gs.blockSize
        tempGroup = pygame.sprite.Group()
        tempGroup.add(self.tempBlock)
        tempGroup.add(self.tempBlock2)
        tempGroup.add(self.tempBlock3)
        tempGroup.add(self.tempBlock4)
        self.assertEqual(self.Cam.draw(self.screen, tempGroup), [self.tempBlock])


class testChunks(unittest.TestCase):
    testWorld = pygame.sprite.Group()
    TempPlayer = ph.Player((gs.width / 2 - gs.blockSize * 4,
                            - gs.blockSize * 2), 24)

    def test_generation(self):
        gs.generatedChunks[-1] = CG.generateChunk(-gs.CHUNK_SIZE[0], self.testWorld)
        gs.generatedChunks[0] = CG.generateChunk(0, self.testWorld)
        gs.generatedChunks[1] = CG.generateChunk(gs.CHUNK_SIZE[0], self.testWorld)
        self.assertIsInstance(gs.generatedChunks[-1], pygame.sprite.Group)
        self.assertIsInstance(gs.generatedChunks[0], pygame.sprite.Group)
        self.assertIsInstance(gs.generatedChunks[1], pygame.sprite.Group)

    def test_Load_Unload(self):
        gs.generatedChunks[-1] = CG.generateChunk(-gs.CHUNK_SIZE[0], self.testWorld)
        gs.generatedChunks[0] = CG.generateChunk(0, self.testWorld)
        gs.generatedChunks[1] = CG.generateChunk(gs.CHUNK_SIZE[0], self.testWorld)
        testChunk = [-1, 0, 1]
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld)
        self.assertEqual(testChunk, gs.visibleChunks)
        self.TempPlayer.rect.x += gs.CHUNK_SIZE[0] * gs.blockSize
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld)
        self.assertNotEqual(testChunk, gs.visibleChunks)
        self.assertEqual([0, 1, 2], gs.visibleChunks)
        self.TempPlayer.rect.x -= gs.CHUNK_SIZE[0] * gs.blockSize
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld)
        self.assertEqual(testChunk, gs.visibleChunks)
        self.TempPlayer.rect.x -= gs.CHUNK_SIZE[0] * gs.blockSize
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld)
        self.assertNotEqual(testChunk, gs.visibleChunks)
        self.assertEqual([-2, -1, 0], gs.visibleChunks)
        self.TempPlayer.rect.x -= gs.CHUNK_SIZE[0] * gs.blockSize
        CH.checkChunkUpdates(self.TempPlayer, self.testWorld)
        self.assertNotEqual(testChunk, gs.visibleChunks)
        self.assertEqual([-3, -2, -1], gs.visibleChunks)


class TestBreakPlace(unittest.TestCase):
    TempPlayer = ph.Player((8 * gs.blockSize, 8 * gs.blockSize), 24)
    pos = (8, 8)
    tempBlock = block.Block(gs.blockSize, (8 * gs.blockSize, 7 * gs.blockSize), 0, textureNames[itemIDs[0]],
                            1, breakSpeed[0])
    tempItem = itemArr[12]  # Item("Wooden Pickaxe", 11)
    tempItem.itemHardness = 3
    spriteGroup = pygame.sprite.Group()
    spriteGroup.add(tempBlock)

    # hotbar=ih.getHotBar()
    # ih.addBlock(tempBlock)
    # print(ih.getSelected())
    def test_getPos(self):
        self.assertEqual(gs.getPos(self.pos), (0, 0))

    # def test_Distance(self):
    #    self.assertEqual(int(gs.distance(self.TempPlayer,self.pos)),226)
    def test_checkBreak(self):
        self.assertTrue(bph.checkBreakable(self.tempBlock, self.tempItem))
        self.tempItem.itemHardness = 0
        self.assertFalse(bph.checkBreakable(self.tempBlock, self.tempItem))
        '''removed depricated function
   def test_notEmpty(self):
      #self.hotbar.append(self.tempBlock)
      #self.assertTrue(bph.notEmpty(self.hotbar[0]))
      print("ADD THIS")
      '''

    def test_breakBlock(self):
        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 0, textureNames["Grass Block"],
                                blockHardness[0], breakSpeed[0])
        self.spriteGroup.add(tempBlock)
        gs.generatedChunks[0] = self.spriteGroup
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        inventory = ih.getInv()
        found = False
        for i in range(len(inventory)):
            if (inventory[i].itemID == 0 and inventory[i].getCount() == 1):
                ih.selected = i
                ih.decrease()
                found = True
        self.assertTrue(found)
        tempBlock = block.Block(gs.blockSize, (30 * gs.blockSize, 30 * gs.blockSize), 0, textureNames["Grass Block"],
                                blockHardness[0], breakSpeed[0])
        self.spriteGroup.add(tempBlock)
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        inventory = ih.getInv()
        found = False
        for i in range(len(inventory)):
            if (inventory[i].itemID == 0 and inventory[i].getCount() == 1):
                found = True
        self.assertFalse(found)
        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 2, textureNames["Stone Block"],
                                blockHardness[2], breakSpeed[2])
        self.spriteGroup.add(tempBlock)
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        inventory = ih.getInv()
        found = False
        for i in range(len(inventory)):
            if (inventory[i].itemID == 2 and inventory[i].getCount() == 1):
                found = True
        self.assertFalse(found)
        tempItem = itemArr[12]  # Item("Wooden Pickaxe", 11)
        ih.addItem(tempItem)
        bph.blockBreak((9 * gs.blockSize, 9 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        inventory = ih.getInv()
        found = False
        for i in range(len(inventory)):
            if (inventory[i].itemID == 2 and inventory[i].getCount() == 1):
                ih.decreaseSpec(tempItem.itemID)
                ih.selected = i
                ih.decrease()
                found = True
        self.assertTrue(found)

    def test_getBlockFromPos(self):
        craftableBlock = block.Block(gs.blockSize, (10 * gs.blockSize, 10 * gs.blockSize), 5,
                                     textureNames[itemIDs[0]], 1, breakSpeed[5])
        self.spriteGroup.add(craftableBlock)
        self.assertEqual(craftableBlock.itemID,
                         bph.getBlockFromPos((10 * gs.blockSize, 10 * gs.blockSize), self.spriteGroup).itemID)
        self.assertEqual(-1, bph.getBlockFromPos((200 * gs.blockSize, 10 * gs.blockSize), self.spriteGroup).itemID)

    def test_blockPlace(self):

        craftableBlock = block.Block(gs.blockSize, (10 * gs.blockSize, 10 * gs.blockSize), 5,
                                     textureNames[itemIDs[0]], 1, breakSpeed[5])
        self.spriteGroup.add(craftableBlock)
        bph.blockPlace(self.pos, self.spriteGroup, self.TempPlayer, True)
        self.assertFalse(gs.drawCrafting)
        bph.blockPlace((craftableBlock.rect.x, craftableBlock.rect.y), self.spriteGroup, self.TempPlayer, True)
        self.assertTrue(gs.drawCrafting)
        self.pos = (8000, 8000)
        bph.blockPlace(self.pos, self.spriteGroup, self.TempPlayer, True)
        # empties the inventory
        inventory = ih.getInv()
        for i in range(len(inventory)):
            ih.selected = i
            if (ih.getSelected().itemID != -1):
                for j in range(len(ih.getSelected().getCount())):
                    ih.decrease()
        ih.selected = 0
        gs.generatedChunks[0] = self.spriteGroup
        tempBlock = block.Block(gs.blockSize, (15 * gs.blockSize, 15 * gs.blockSize), 43, textureNames["Iron Ore"],
                                blockHardness[43], breakSpeed[43])
        ih.addBlock(tempBlock)
        self.TempPlayer.rect.x = 8 * gs.blockSize
        self.TempPlayer.rect.y = 8 * gs.blockSize
        bph.blockPlace((6 * gs.blockSize, 6 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        found = False
        inventory = ih.getInv()
        for i in range(len(inventory)):
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True
        ih.addBlock(tempBlock)
        ih.addBlock(tempBlock)
        bph.blockPlace((5 * gs.blockSize, 6 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        found = False
        inventory = ih.getInv()
        for i in range(len(inventory)):
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True
        bph.blockPlace((8 * gs.blockSize, 8 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        found = False
        inventory = ih.getInv()
        for i in range(len(inventory)):
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True
        self.assertTrue(found)
        bph.blockPlace((800000 * gs.blockSize, 800000 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        found = False
        inventory = ih.getInv()
        for i in range(len(inventory)):
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True
        self.assertTrue(found)
        bph.blockPlace((5 * gs.blockSize, 6 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        found = False
        inventory = ih.getInv()
        for i in range(len(inventory)):
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True
        self.assertTrue(found)
        bph.blockPlace((8 * gs.blockSize, 10 * gs.blockSize), self.spriteGroup, self.TempPlayer, True)
        found = False
        inventory = ih.getInv()
        for i in range(len(inventory)):
            if (inventory[i].itemID == 43 and inventory[i].getCount() == 1):
                found = True
        self.assertFalse(found)


class TestInvinventorySlots(unittest.TestCase):
    ins = InventorySlots.slot("red", 10, 20, 30, 40)

    def test_everything(self):
        self.assertEqual(self.ins.width, 30)
        self.assertEqual(self.ins.height, 40)
        self.assertEqual(self.ins.rect.x, 10)
        self.assertEqual(self.ins.rect.y, 20)
        self.assertEqual(self.ins.image.get_width(), 30)
        self.assertEqual(self.ins.image.get_height(), 40)


class TestPortal(unittest.TestCase):
    port = Portal.Portal(gs.blockSize, (8, 7), 26, textureNames[itemIDs[0]], 999)

    def test_init(self):
        self.assertEqual(self.port.textureName, textureNames[itemIDs[0]])
        self.assertEqual(self.port.itemID, 26)
        x = 8 - 4 * gs.blockSize
        y = 7 - 8 * gs.blockSize
        self.assertEqual(self.port.blockPosition, [x, y])
        self.assertEqual(self.port.rect.x, 8 - 0.4 * gs.blockSize)
        self.assertEqual(self.port.rect.y, 7 - 1 * gs.blockSize)

    def test_getHardness(self):
        self.assertEqual(self.port.getHardness(), 999)


# need to change tooltype and reqtooltype and drops when we used it
class TestItemNew(unittest.TestCase):
    def test_getDrop(self):
        newItems = itemNew.Item(9, "Bigblock", 100, 3, 3, "axe", "pickaxe", "texture", False, "drops")
        self.assertEqual(newItems.getCount(), 0)
        newItems.increase()
        self.assertEqual(newItems.getCount(), 1)
        newItems.decrease()
        self.assertEqual(newItems.getCount(), 0)

        self.assertEqual(int, type(newItems.itemID))
        self.assertEqual(str, type(newItems.itemDisplayName))
        self.assertEqual(int, type(newItems.breakTime))
        self.assertEqual(int, type(newItems.blockHardness))
        self.assertEqual(int, type(newItems.itemHardness))
        self.assertEqual(str, type(newItems.reqToolType))
        self.assertEqual(str, type(newItems.toolType))
        self.assertEqual(str, type(newItems.texture))
        self.assertEqual(bool, type(newItems.isPlaceable))
        self.assertEqual(str, type(newItems.drops))

        self.assertEqual(newItems.getItemId(), 9)
        self.assertEqual(newItems.getItemName(), "Bigblock")
        self.assertEqual(newItems.getBreakTime(), 100)
        self.assertEqual(newItems.getBlockHardness(), 3)
        self.assertEqual(newItems.getItemHardness(), 3)
        self.assertEqual(newItems.getReqToolType(), "axe")
        self.assertEqual(newItems.getToolType(), "pickaxe")
        self.assertEqual(newItems.getTexture(), "texture")
        self.assertEqual(newItems.getIsPlaceable(), False)
        self.assertEqual(newItems.getDrop(), "drops")


'''
class TestItemHandler (unittest.TestCase):
       def test_populateDictionaries(self):
         self.assertEqual(populateDictionaries(),None); 
         self.assertEqual(dict,  type(itemHandler.itemIDs));
#unittest.TestLoader.sortTestMethodsUsing=None
'''


# commented out because its complaining that neither populate dictionaries and itemhandler dont exist
class testMinecraftEnv(unittest.TestCase):
    NullItem = itemArr[0]  # Item("null", -1)
    ih.invArray=np.full(40, NullItem, dtype=itemNew.Item)
    ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=0, seed="555")
    

    def testStartModes(self):
        for i in itemArr:
            if(i.amount>0):
                i.amount=0
        ih.invArray=np.full(40, self.NullItem, dtype=itemNew.Item)
        self.ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=1)
        self.assertEqual(ih.getItemCount(11), 1)  # check if the game starts witha wooden pickaxe
        self.assertEqual(ih.getItemCount(8), 4)  # and 4 wooden planks
        ih.invArray = np.full(40, self.NullItem, dtype=itemNew.Item)
        for i in itemArr:
            if(i.amount>0):
                i.amount=0
        self.ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=2)
        self.assertEqual(ih.getItemCount(11), 1)  # check if the game starts witha wooden pickaxe
        self.assertEqual(ih.getItemCount(8), 4)  # and 4 wooden planks
        self.assertEqual(ih.getItemCount(16), 1)  # check if the game starts witha Stone pickaxe
        self.assertEqual(ih.getItemCount(50), 1)  # check if the game starts with a diamon
        self.assertEqual(ih.getItemCount(53), 1)  # check if the game starts with an emerald
        ih.invArray = np.full(40, self.NullItem, dtype=itemNew.Item)

    def testActionSpaceMovement(self):
        self.ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=0, seed="555")
        prevpos = (0, 0)
        currpos = self.ENV.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.action(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.player.getPlayerPos()
        currpos = self.ENV.player.getPlayerPos()
        self.ENV.action(gs.actionSpace["MOVEMENT"][1])
        self.assertNotEqual(currpos, self.ENV.player.getPlayerPos())
        self.ENV.action(gs.actionSpace["MOVEMENT"][0])
        self.ENV.action(gs.actionSpace["MOVEMENT"][0])
        self.ENV.action(gs.actionSpace["MOVEMENT"][0])
        currpos = self.ENV.player.getPlayerPos()
       # self.ENV.action(gs.actionSpace["MOVEMENT"][3])
       # self.ENV.action(gs.actionSpace["MOVEMENT"][3])
       # self.ENV.action(gs.actionSpace["MOVEMENT"][3])
        self.ENV.action(gs.actionSpace["MOVEMENT"][3])

        self.ENV.player.update(2,self.ENV.worldBlocks)
        #self.assertNotEqual(currpos, self.ENV.player.getPlayerPos())
        self.ENV.action(gs.actionSpace["MOVEMENT"][0])
        currpos = self.ENV.player.getPlayerPos()
        self.ENV.action(gs.actionSpace["MOVEMENT"][2])
        self.assertNotEqual(currpos, self.ENV.player.getPlayerPos())

        prevpos = (0, 0)  # wait for the player to stop jumping
        currpos = self.ENV.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.action(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.player.getPlayerPos()

        self.ENV.action(gs.actionSpace["MOVEMENT"][0])
        currpos = self.ENV.player.getPlayerPos()
        self.ENV.action(gs.actionSpace["MOVEMENT"][4])
        self.assertNotEqual(currpos, self.ENV.player.getPlayerPos())

        prevpos = (0, 0)  # wait for the player to stop jumping
        currpos = self.ENV.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.action(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.player.getPlayerPos()
        self.ENV.action(gs.actionSpace["MOVEMENT"][0])
        currpos = self.ENV.player.getPlayerPos()
        self.ENV.action(gs.actionSpace["MOVEMENT"][5])
        self.assertNotEqual(currpos, self.ENV.player.getPlayerPos())

        prevpos = (0, 0)  # wait for the player to stop jumping
        currpos = self.ENV.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.action(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.player.getPlayerPos()

    def testActionSpaceHotBar(self):
        self.ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=0, seed="555")
        ih.selected = 0
        for i in range(40):
            self.ENV.action(gs.actionSpace["HOTBAR"][i])
            self.assertEqual(ih.selected, i)

    def testActionSpaceCrafting(self):
        self.ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=0, seed="555")
        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 7, textureNames["Oak Log"],
                                blockHardness[7], breakSpeed[7])
        ih.addBlock(tempBlock)
        inv = ih.getInv()
        found = False
        for i in inv:
            if (i.itemID == 8):  # see if there are logs in the inventory
                found = True
                break
        self.assertFalse(found)
        self.ENV.action(gs.actionSpace["CRAFTING"][0])
        found = False
        for i in inv:
            if (i.itemID == 8):  # see if there are logs in the inventory
                found = True
                break
        self.assertTrue(found)
        ih.invArray = np.full(40, self.NullItem, dtype=itemNew.Item)

    def testActionSpacePlaceAndBreak(self):
        self.ENV = MCENV.MinePy(render_mode="rgb_array", easyStart=0, seed="555")
        prevpos = (0, 0)
        currpos = self.ENV.player.getPlayerPos()
        while (prevpos != currpos):
            self.ENV.action(gs.actionSpace["MOVEMENT"][0])  # forces the players position to be set to the ground
            prevpos = currpos
            currpos = self.ENV.player.getPlayerPos()

        tempBlock = block.Block(gs.blockSize, (9 * gs.blockSize, 9 * gs.blockSize), 7, textureNames["Oak Log"],
                                blockHardness[7], breakSpeed[7])
        for i in range(5):
            ih.addBlock(tempBlock)
        self.assertEqual(ih.getItemCount(7), 5)  # check that there are 10 logs in the inventory
        inv = ih.getInv()
        for i in range(len(inv)):
            if (inv[i].itemID == 7):
                ih.selected = i
                break
        count = 5
        for i in range(5):
            count -= 1
            self.ENV.action(gs.actionSpace["WORLD"][10 + i])
            self.assertEqual(ih.getItemCount(7), count)
        count = 0
        for i in range(5):
            count += 1
            self.ENV.action(gs.actionSpace["WORLD"][i])  # break blocks around the player
            self.assertEqual(ih.getItemCount(7), count)  # see if it got readded to the inventory
        ih.invArray = np.full(40, self.NullItem, dtype=itemNew.Item)


unittest.main()

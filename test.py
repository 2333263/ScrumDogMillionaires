import unittest
from numpy import ndarray
import Camera
import item 
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
import copy
import soundHandler
#update test for sound
class TestItem(unittest.TestCase):
   tempItem = item.Item("Grass", 0)
   tempItem1 = item.Item("Dirt", 0,20)
   def test_itemID(self):
      self.assertIsInstance(self.tempItem.itemID, int)
      self.assertGreaterEqual(self.tempItem.itemID, 0)
      self.assertLessEqual(self.tempItem.itemID, len(gs.itemIDs) + 1)
      self.assertEqual(self.tempItem.getItemId(), self.tempItem.itemID)
      self.assertIsInstance(self.tempItem1.itemID, int)
      self.assertGreaterEqual(self.tempItem1.itemID, 0)
      self.assertLessEqual(self.tempItem1.itemID, len(gs.itemIDs) + 1)
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
      self.assertIsInstance(self.tempItem.itemName, str)
      self.assertEqual(self.tempItem.getItemName(),"Grass")
      self.assertIsInstance(self.tempItem1.itemName, str)
      self.assertEqual(self.tempItem1.getItemName(),"Dirt")
   def test_Hardness(self):
      self.assertEqual(self.tempItem.getHardness(),0)
      self.assertEqual(self.tempItem1.getHardness(),20)

class TestBlock(unittest.TestCase):
   tempBlock = block.Block(gs.blockSize, (0, 0), 0, gs.textureNames[gs.itemIDs[0]],0)
   def test_itemIDs(self):
      self.assertIsInstance(self.tempBlock.itemID, int)
      self.assertGreaterEqual(self.tempBlock.itemID, 0)
      self.assertLessEqual(self.tempBlock.itemID, len(gs.itemIDs) + 1)

   def test_positions(self):
      self.assertGreaterEqual(self.tempBlock.blockPosition[0], 0)
      self.assertGreaterEqual(self.tempBlock.blockPosition[1], 0)

      self.assertLessEqual(self.tempBlock.blockPosition[0], gs.width)
      self.assertLessEqual(self.tempBlock.blockPosition[1], gs.height)

   def test_texture(self):
      self.assertIsInstance(self.tempBlock.textureName,  str)
      self.assertIsInstance(self.tempBlock.rect, pygame.rect.Rect)
      #Add check for texture object

   def test_hardness(self):
      self.assertEqual(self.tempBlock.getHardness(),0)
class TestCraftingButton(unittest.TestCase):
   tempButton = CraftButtonHandler.Button(0, (0, 0), 50, 50)
   pygame.init()
   def test_itemIDs(self):
      self.assertIsInstance(self.tempButton.itemID, int)
      self.assertGreaterEqual(self.tempButton.itemID, 0)
      self.assertLessEqual(self.tempButton.itemID, len(gs.itemIDs) + 1)
   
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
   TempPlayer=ph.Player((8*gs.blockSize, 8*gs.blockSize), 24)
   def test_innit(self):
      self.assertEqual(self.TempPlayer.rect.x,8*gs.blockSize)
      self.assertEqual(self.TempPlayer.rect.y,8*gs.blockSize)
      self.assertTrue(type(self.TempPlayer) is ph.Player)

   def test_pos(self):
      self.assertEqual(self.TempPlayer.getPlayerPos(),(8*gs.blockSize,8*gs.blockSize))
#this is a comment
   def test_MoveX(self):
      #empty={}
      #self.TempPlayer.MoveOnX(empty)
      #self.assertNotEqual(len(self.TempPlayer.keys),0)
      self.simulatedKeys={
         pygame.K_LEFT: False, 
         pygame.K_RIGHT: False,
         pygame.K_a: False,
         pygame.K_d: False
      }
      self.simulatedKeys[pygame.K_LEFT]=True
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,-2)
      self.simulatedKeys[pygame.K_LEFT]=False
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,0)

      self.simulatedKeys[pygame.K_a]=True
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,-2)
      self.simulatedKeys[pygame.K_a]=False
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,0)

      self.simulatedKeys[pygame.K_RIGHT]=True
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,2)
      self.simulatedKeys[pygame.K_RIGHT]=False
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,0)

      self.simulatedKeys[pygame.K_d]=True
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,2)
      self.simulatedKeys[pygame.K_d]=False
      self.TempPlayer.MoveOnX(self.simulatedKeys)
      self.assertEqual(self.TempPlayer.direction.x,0)

   def test_gravity(self):
      self.TempPlayer.useGravity()
      self.assertEqual(self.TempPlayer.direction.y,self.TempPlayer.gravity)
      self.TempPlayer.direction.y=0

   def test_jump(self):
      #jumped is false by default in case we spawn the player above the world
      self.assertEqual(self.TempPlayer.jumped,False)
      self.TempPlayer.jump()
      self.assertEqual(self.TempPlayer.jumped,True)
      self.assertEqual(self.TempPlayer.direction.y,-2.5)
      self.TempPlayer.jumped=False

   def test_jumping_acceleration(self):
      self.TempPlayer.jumpArc()
      #check if player is jumped get set to false when direction.y==0
      self.assertEqual(self.TempPlayer.jumped,False)
      self.TempPlayer.direction.y=-5
      #testing if the grabity acceleration changes 
      self.TempPlayer.jumpArc()
      self.assertEqual(self.TempPlayer.direction.y,-5+self.TempPlayer.gravity/20)
      self.TempPlayer.direction.y=0
#NEED TO BE REWRITTEN 
   def test_update(self):
      tempBlock = block.Block(gs.blockSize, (8, 7), 0, gs.textureNames[gs.itemIDs[0]],0)
      tempGroup=pygame.sprite.Group()
      tempGroup.add(tempBlock)
      self.TempPlayer.jumped=True
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.jumped,False) 
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.y,2.0)
      for x in tempGroup:
         x.blockPosition=(8*gs.blockSize,10*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.y,2.0)
      self.TempPlayer.direction.x=-1
      for x in tempGroup:
         x.blockPosition=(7*gs.blockSize,8*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,-1.0)
      self.TempPlayer.direction.x=-1
      for x in tempGroup:
         x.blockPosition=(7*gs.blockSize,9*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,-1.0)
      self.TempPlayer.direction.x=1
      for x in tempGroup:
         x.blockPosition=(9*gs.blockSize,8*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,1.0)
      self.TempPlayer.direction.x=1
      for x in tempGroup:
         x.blockPosition=(9*gs.blockSize,9*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,1.0)
      self.TempPlayer.jumped=True
      for x in tempGroup:
         x.blockPosition=(8*gs.blockSize,8*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.y,2.1)
      self.TempPlayer.direction.x=1
      self.TempPlayer.direction.y=1
      tempPosX=self.TempPlayer.rect.x
      tempPosY=self.TempPlayer.rect.y
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.rect.y,tempPosY+1)
      self.assertEqual(self.TempPlayer.rect.x,tempPosX+1)
      self.TempPlayer.rect.x=tempPosX
      self.TempPlayer.rect.y=tempPosY
      self.TempPlayer.update(2,tempGroup)
      self.assertEqual(self.TempPlayer.rect.y,tempPosY+2)
      self.assertEqual(self.TempPlayer.rect.x,tempPosX+2)

   def test_StopOnX(self):
      self.TempPlayer.stopMoveOnX()
      self.assertEqual(self.TempPlayer.direction.x,0)

class TestCraftingMenu (unittest.TestCase):
      screen = pygame.display
      crafter = CraftingMenu.Crafting(screen)
      def test_relativeSize(self):
             self.assertTrue(self.crafter.relativeSize >= 0 and self.crafter.relativeSize <= gs.blockSize*3)
      def test_allItems(self):
             self.assertIsInstance(list(),  type(self.crafter.allItems))
      def test_menuBackround(self):
             self.assertIsInstance(pygame.sprite.Group(),  type(self.crafter.menuBackround))
      def test_craftables(self):
             self.assertIsInstance(pygame.sprite.Group(),  type(self.crafter.craftables))
      def test_itemName(self):
             self.assertIsInstance(pygame.sprite.GroupSingle(),  type(self.crafter.itemName))
      def test_itemRecipe(self):
             self.assertIsInstance(pygame.sprite.Group(),  type(self.crafter.itemRecipe))
      def test_itemsNeeded(self):
             self.assertIsInstance(dict(),  type(self.crafter.itemsNeeded))
      def test_canCraft(self):
             self.assertEqual(self.crafter.canCraft, False)
      def test_createdItem(self):
             self.assertGreaterEqual(self.crafter.createdItem, -1)
      def test_craftButton(self):#10
             self.assertIsInstance(pygame.sprite.Group(),  type(self.crafter.craftButton))
#       def test_makeScreen(self):
#              self.assertIsInstance(NULL,  type(self.crafter.makeBackground()))
      def test_makeBackground(self):
             self.assertIsInstance(pygame.sprite.Group(),  type(self.crafter.makeBackground()))
      def test_populatePossibleItems(self):
             self.assertIsInstance(pygame.sprite.Group(),  type(self.crafter.populatePossibleItems()))
      def test_populateRecipe(self):
             self.crafter.populateRecipe(self.crafter.craftables)
             self.crafter.populateRecipe(self.crafter.craftables)
             self.crafter.populateRecipe(self.crafter.craftables)
             self.crafter.populateRecipe(self.crafter.craftables)
             self.assertTrue(self.crafter.itemRecipe.__sizeof__() >= 0)
      def test_resetTable(self):
             self.crafter.resetTable();
             self.assertEqual(self.crafter.itemRecipe.has(), False)
             self.assertEqual(self.crafter.craftButton.has(), False)
      def test_checkClick(self):
             self.crafter.checkClick((0,0))
             self.assertTrue(self.crafter.craftButton.has()>= 0)
      def test_makeItem(self):
             self.crafter.makeItem((0,0))
             self.assertEqual(self.crafter.itemRecipe.has(), False)
             self.assertEqual(self.crafter.craftButton.has(), False)
      def test_isCraftable(self):
             for menuItem in self.crafter.craftables:
                    if(self.crafter.isCraftable(menuItem.itemID,ih.getInv())):
                          self.assertIsInstance(True,  type(self.crafter.isCraftable(menuItem.itemID,ih.getInv())))
                    else:
                          self.assertIsInstance(False,  type(self.crafter.isCraftable(menuItem.itemID,ih.getInv())))
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

      self.assertIsInstance(gs.itemIDs, dict)
      self.assertIsInstance(gs.craftingIDs, dict)
      self.assertIsInstance(gs.converterIDs, dict)
      self.assertIsInstance(gs.textureNames, dict)

      self.assertIsInstance(gs.immovableBlocks, list)
      self.assertIsInstance(gs.clickableBlocks, list)

class TestInventoryHandler(unittest.TestCase):
    hotbar=ih.getInv()
    tempBlock = block.Block(gs.blockSize, (8, 7), 0, gs.textureNames[gs.itemIDs[0]],0)
    tempBlock2=block.Block(gs.blockSize, (20, 7), 1, gs.textureNames[gs.itemIDs[1]],0)
    tempBlock3=block.Block(gs.blockSize, (29, 7), 2, gs.textureNames[gs.itemIDs[1]],0)
    tempBlock4=block.Block(gs.blockSize, (50, 7), 3, gs.textureNames[gs.itemIDs[1]],0)
    tempItem = item.Item("Cloud", 4)
    # screen=pygame.Surface((gs.blockSize*gs.noXBlocks, gs.blockSize*gs.noYBlocks))
    def test_AddBlock(self):
       ih.addBlock(self.tempBlock)
       #self.hotbar=ih.getHotBar()
       self.assertEqual(self.hotbar[0].itemID,self.tempBlock.itemID)
       self.assertEqual(self.hotbar[0].getCount(),1)
       ih.addBlock(self.tempBlock)
       #self.hotbar=ih.getHotBar()
       self.assertEqual(self.hotbar[0].getCount(),2)
    def test_Decrease(self):
       #selected is 0 currently
       self.assertEqual(self.hotbar[0].getCount(),2)
       ih.decrease()
       self.assertEqual(self.hotbar[0].getCount(),1)
       ih.addBlock(self.tempBlock2)
       self.assertEqual(self.hotbar[1].getCount(),1)
       ih.selected=1
       ih.decrease()
       self.assertNotIn(self.tempBlock2,self.hotbar)
       self.assertEqual(self.hotbar[1].getCount(),0)
       ih.decrease()
       self.assertEqual(self.hotbar[1], ih.NullItem)
    def test_DecreaseSpec(self):
       ih.addBlock(self.tempBlock)
       ih.addBlock(self.tempBlock2)
       ih.addBlock(self.tempBlock2)
       ih.addBlock(self.tempBlock3)
       ih.addBlock(self.tempBlock3)
       self.assertEqual(self.hotbar[1].getCount(),2)
       ih.decreaseSpec(self.tempBlock2.itemID)
       self.assertEqual(self.hotbar[1].getCount(),1)
       ih.decreaseSpec(self.tempBlock2.itemID)
       self.assertEqual(self.hotbar[1], ih.NullItem)
       self.assertNotEqual(self.hotbar[1].itemID,self.tempBlock2.itemID)
    def test_Selected(self):
       ih.selected=0
       self.assertEqual(ih.selected,0)
       self.assertEqual(ih.getSelected().itemID,self.tempBlock.itemID)
       self.assertEqual(item.Item,  type(ih.getSelected()))
       ih.selected=1
       self.assertEqual(ih.selected,1)
       ih.addBlock(self.tempBlock2)
       self.assertEqual(ih.getSelected().itemID,self.tempBlock2.itemID)
   
    def test_selectNext(self):
       ih.selected=0
       ih.selectNext()
       self.assertEqual(ih.selected,1)
       self.assertEqual(ih.getSelected().itemID,self.tempBlock2.itemID)
       ih.selectNext()
       self.assertEqual(ih.selected,2)
       self.assertEqual(ih.getSelected().itemID,self.tempBlock3.itemID)
    def test_selectPrevious(self):  
       ih.selectPrevious()
       self.assertEqual(ih.selected,1)
       self.assertEqual(ih.getSelected().itemID,self.tempBlock2.itemID)
       ih.selectPrevious()
       self.assertEqual(ih.selected,0)
       self.assertEqual(ih.getSelected().itemID,self.tempBlock.itemID)
    def test_getInv(self):
           self.assertEqual(ndarray,  type(ih.getInv()))
    def test_getItemCount(self):
       ih.addBlock(self.tempBlock)
       self.assertEqual(ih.getItemCount(self.tempBlock.itemID),3)
       self.assertEqual(ih.getItemCount(self.tempBlock2.itemID),1)
    def test_addItem(self):
       ih.addItem(self.tempItem)
       ih.addItem(self.tempItem)
       self.assertEqual(self.hotbar[3].itemID,self.tempItem.itemID)
    #def test_drawInv(self):
    #   try:
    #       ih.drawHotBar(self.screen)
    #       self.assertTrue(True)
    #    except:
    #       self.assertTrue(False)
    def test_initGroup(self):
       ih.initGroup()
       self.assertTrue(ih.hotBarrSprite.__len__() >0)
       self.assertTrue(ih.slots.__len__() >0)  

class TestCamera(unittest.TestCase):
   TempPlayer=ph.Player((8*gs.blockSize, 8*gs.blockSize), 24)
   Cam=Camera.Camera(TempPlayer)
   #pygame.display.set_mode((1280, 720))
   screen = pygame.Surface((gs.blockSize, gs.blockSize))
   tempBlock = block.Block(gs.blockSize, (8, 7), 0, gs.textureNames[gs.itemIDs[0]],0)
   tempBlock2=block.Block(gs.blockSize, (20, 7), 1, gs.textureNames[gs.itemIDs[1]],0)
   tempBlock3=block.Block(gs.blockSize, (29, 7), 2, gs.textureNames[gs.itemIDs[1]],0)
   tempBlock4=block.Block(gs.blockSize, (50, 7), 3, gs.textureNames[gs.itemIDs[1]],0)
   def test_Offset(self):
      self.Cam.scroll()
      #self.assertEqual(self.Cam.offset,pygame.math.Vector2(-558,-176))
      self.assertEqual(self.Cam.getOffsets(),self.Cam.offset)
   def test_Collide(self):
      self.assertFalse(self.Cam.isColideable(self.tempBlock))
      self.tempBlock.rect.x=8*gs.blockSize
      self.tempBlock.rect.y=8*gs.blockSize
      self.assertTrue(self.Cam.isColideable(self.tempBlock))
   def test_onScreen(self):
      self.assertTrue(self.Cam.isOnScreen(self.tempBlock))
      self.tempBlock.rect.x=1000
      self.tempBlock.rect.y=1000
      #self.assertFalse(self.Cam.isOnScreen(self.tempBlock))
   def test_draw(self):
      self.tempBlock.rect.x=8*gs.blockSize
      self.tempBlock.rect.y=8*gs.blockSize
      tempGroup=pygame.sprite.Group()
      tempGroup.add(self.tempBlock)
      tempGroup.add(self.tempBlock2)
      tempGroup.add(self.tempBlock3)
      tempGroup.add(self.tempBlock4)
      self.assertEqual(self.Cam.draw(self.screen,tempGroup),[self.tempBlock])

class testChunks(unittest.TestCase):
   testWorld = pygame.sprite.Group()
   TempPlayer=ph.Player((gs.width/2 - gs.blockSize * 4,
                      - gs.blockSize*2), 24)
   def test_generation(self):
      gs.generatedChunks[-1] = CG.generateChunk(-gs.CHUNK_SIZE[0], self.testWorld)
      gs.generatedChunks[0] = CG.generateChunk(0, self.testWorld)
      gs.generatedChunks[1] = CG.generateChunk(gs.CHUNK_SIZE[0], self.testWorld)
      self.assertIsInstance(gs.generatedChunks[-1],pygame.sprite.Group)
      self.assertIsInstance(gs.generatedChunks[0],pygame.sprite.Group)
      self.assertIsInstance(gs.generatedChunks[1],pygame.sprite.Group)
   def test_Load_Unload(self):
      gs.generatedChunks[-1] = CG.generateChunk(-gs.CHUNK_SIZE[0], self.testWorld)
      gs.generatedChunks[0] = CG.generateChunk(0, self.testWorld)
      gs.generatedChunks[1] = CG.generateChunk(gs.CHUNK_SIZE[0], self.testWorld)
      testChunk=[-1,0,1]
      CH.checkChunkUpdates(self.TempPlayer,self.testWorld)
      self.assertEqual(testChunk,gs.visibleChunks)
      self.TempPlayer.rect.x+=gs.CHUNK_SIZE[0]*gs.blockSize
      CH.checkChunkUpdates(self.TempPlayer,self.testWorld)
      self.assertNotEqual(testChunk,gs.visibleChunks)
      self.assertEqual([0,1,2],gs.visibleChunks)
      self.TempPlayer.rect.x-=gs.CHUNK_SIZE[0]*gs.blockSize
      CH.checkChunkUpdates(self.TempPlayer,self.testWorld)
      self.assertEqual(testChunk,gs.visibleChunks)
      self.TempPlayer.rect.x-=gs.CHUNK_SIZE[0]*gs.blockSize
      CH.checkChunkUpdates(self.TempPlayer,self.testWorld)
      self.assertNotEqual(testChunk,gs.visibleChunks)
      self.assertEqual([-2,-1,0],gs.visibleChunks)
      self.TempPlayer.rect.x-=gs.CHUNK_SIZE[0]*gs.blockSize
      CH.checkChunkUpdates(self.TempPlayer,self.testWorld)
      self.assertNotEqual(testChunk,gs.visibleChunks)
      self.assertEqual([-3,-2,-1],gs.visibleChunks)
class TestBreakPlace(unittest.TestCase):
   TempPlayer=ph.Player((8*gs.blockSize, 8*gs.blockSize), 24)
   pos=(8,8)
   tempBlock = block.Block(gs.blockSize, (8*gs.blockSize, 7*gs.blockSize), 0, gs.textureNames[gs.itemIDs[0]],1)
   tempItem = item.Item("Wooden Pickaxe", 3)
   tempItem.hardness=3
   spriteGroup=pygame.sprite.Group()
   spriteGroup.add(tempBlock)
  # hotbar=ih.getHotBar()
  # ih.addBlock(tempBlock)
  # print(ih.getSelected())
   def test_getPos(self):
      self.assertEqual(gs.getPos(self.pos),(0,0))
   # def test_Distance(self):
   #    self.assertEqual(int(gs.distance(self.TempPlayer,self.pos)),226)
   def test_checkBreak(self):
      self.assertTrue(bph.checkBreakable(self.tempBlock,self.tempItem))
      self.tempItem.hardness=0
      self.assertFalse(bph.checkBreakable(self.tempBlock,self.tempItem))
      '''removed depricated function
   def test_notEmpty(self):
      #self.hotbar.append(self.tempBlock)
      #self.assertTrue(bph.notEmpty(self.hotbar[0]))
      print("ADD THIS")
      '''
  # def test_blockBreak(self):
  #     try:
  ##        newBlock=block.Block(gs.blockSize, (8*gs.blockSize, 8*gs.blockSize), 0, gs.textureNames[gs.itemIDs[0]],0)
  #        self.spriteGroup.add(newBlock)
  #        #ih.addItem(self.tempItem)
  #        self.pos=(8*gs.blockSize,8*gs.blockSize)
  #        bph.blockBreak(self.pos,self.spriteGroup,self.TempPlayer)
  ##        self.assertTrue(True)
  #        ih.decrease()
  #     except Exception as e:
  #        print(e)
  #        self.assertTrue(False)
   def test_blockPlace(self):
      craftableBlock=block.Block(gs.blockSize, (10*gs.blockSize, 10*gs.blockSize), 5, gs.textureNames[gs.itemIDs[0]],1)
      self.spriteGroup.add(craftableBlock)
      bph.blockPlace(self.pos,self.spriteGroup,self.TempPlayer)
      self.assertFalse(gs.drawCrafting)
      bph.blockPlace((craftableBlock.rect.x,craftableBlock.rect.y),self.spriteGroup,self.TempPlayer)
      self.assertTrue(gs.drawCrafting)
      self.pos=(8000,8000)
      bph.blockPlace(self.pos,self.spriteGroup,self.TempPlayer)
      

class TestInvinventorySlots(unittest.TestCase):
    ins = InventorySlots.slot("red", 10, 20, 30, 40)
    def test_everything(self):
       self.assertEqual(self.ins.width,30)
       self.assertEqual(self.ins.height,40)
       self.assertEqual(self.ins.rect.x,10)
       self.assertEqual(self.ins.rect.y,20)
       self.assertEqual(self.ins.image.get_width(),30)
       self.assertEqual(self.ins.image.get_height(),40)
#class TestSoundHandler(unittest.TestCase):
#    def test_testSound(self):
#       self.assertEqual(0.3,  round(soundHandler.getGrassSound().get_volume(),1))
   #     self.assertEqual(0.3,  round(soundHandler.stoneSound.get_volume(),1))
   #     self.assertEqual(0.3,  round(soundHandler.dirtSound.get_volume(),1))
   #     self.assertEqual(0.3,  round(soundHandler.woodSound.get_volume(),1))
   #     self.assertEqual(0.3,  round(soundHandler.leafSound.get_volume(),1))
   #     self.assertEqual(0.1,  round(soundHandler.breakDirtSound.get_volume(),1))
   #     self.assertEqual(0.1,  round(soundHandler.breakGrassSound.get_volume(),1))
   #     self.assertEqual(0.1,  round(soundHandler.breakStoneSound.get_volume(),1))
   #     self.assertEqual(0.1,  round(soundHandler.breakWoodSound.get_volume(),1))
   #     self.assertEqual(0.1,  round(soundHandler.breakLeafSound.get_volume(),1))
   #  def test_playMusic(self):
   #     self.assert_
   #  def test_playBreakSound(self):
   #     pass
   #  def test_playSoundforID(self):
   #     pass
unittest.main()
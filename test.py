import unittest
import item 
import gameSettings as gs
import block
import pygame
import CraftButtonHandler


class TestItem(unittest.TestCase):
   tempItem = item.Item("Grass", 0)
   def test_itemID(self):
      self.assertIsInstance(self.tempItem.itemID, int)
      self.assertGreaterEqual(self.tempItem.itemID, 0)
      self.assertLessEqual(self.tempItem.itemID, len(gs.itemIDs) + 1)

   def test_amount(self):
      self.assertIsInstance(self.tempItem.amount, int)
      self.assertGreaterEqual(self.tempItem.amount, 0)

      oldCount = self.tempItem.amount
      self.tempItem.increase()
      self.assertGreaterEqual(self.tempItem.amount, oldCount)
      self.tempItem.decrease()
      self.assertEqual(self.tempItem.amount, oldCount)
      self.assertEqual(self.tempItem.amount, self.tempItem.getCount())

   def test_name(self):
      self.assertIsInstance(self.tempItem.itemName, str)



class TestBlock(unittest.TestCase):
   tempBlock = block.Block(gs.blockSize, (0, 0), 0, gs.textureNames[gs.itemIDs[0]])
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
      #Add check for texture object


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

   

unittest.main()
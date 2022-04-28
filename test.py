import unittest
import item 
import gameSettings



class TestItem(unittest.TestCase):
   tempItem = item.Item("Grass", 0)
   def test_itemID(self):
      self.assertTrue(type(self.tempItem.itemID) is int)
      self.assertGreaterEqual(self.tempItem.itemID, 0)
      self.assertLessEqual(self.tempItem.itemID, len(gameSettings.itemIDs) + 1)

   def test_amount(self):
      self.assertTrue(type(self.tempItem.amount) is int)
      self.assertGreaterEqual(self.tempItem.amount, 0)

      oldCount = self.tempItem.amount
      self.tempItem.increase()
      self.assertGreaterEqual(self.tempItem.amount, oldCount)
      self.tempItem.decrease()
      self.assertEqual(self.tempItem.amount, oldCount)
      self.assertEqual(self.tempItem.amount, self.tempItem.getCount())

   def test_name(self):
      self.assertTrue(type(self.tempItem.itemName) is str)

   #Need to check the textures load a valid item  


unittest.main()
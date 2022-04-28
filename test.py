import unittest
import item 

# class TestMethods(unittest.TestCase):
#    def test_add(self):
#       tempOneItem = item.Item("Grass", 0)
#       tempTwoItem = item.Item("Grass", 0)
#       self.assertEqual(tempOneItem.itemName, tempTwoItem.itemName)


class TestItem(unittest.TestCase):
   tempItem = item.Item("Grass", 0)
   def test_itemID(self):
      self.assertTrue(type(self.tempItem.itemID) is int)
      
   def test_amount(self):
      self.assertTrue(type(self.tempItem.amount) is int)
      self.assertGreaterEqual(self.tempItem.amount, 0)


unittest.main()
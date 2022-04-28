from typing import List
import unittest
import item 
import gameSettings as gs
import levelGenerator as lg
import block as b
import pygame 



#Testing the level Generator
class TestWorld(unittest.TestCase):
      
      def test_getBlock(self):
            self.assertIsInstance(pygame.sprite.Group(),  type(lg.getBlocks(gs.levelName)))



unittest.main()
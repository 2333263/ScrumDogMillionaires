from time import sleep
import unittest
import item 
import playerHandler as ph
import gameSettings as gs
import pygame
import block
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



class TestPlayer(unittest.TestCase):
   TempPlayer=ph.Player((8*gs.blockSize, 8*gs.blockSize), 24)
   def test_innit(self):
      self.assertEqual(self.TempPlayer.rect.x,8*gs.blockSize)
      self.assertEqual(self.TempPlayer.rect.y,8*gs.blockSize)
      self.assertTrue(type(self.TempPlayer) is ph.Player)

   def test_pos(self):
      self.assertEqual(self.TempPlayer.getPlayerPos(),(8*gs.blockSize,8*gs.blockSize))

   def test_MoveX(self):
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
      self.assertEqual(self.TempPlayer.direction.y,-2)
      self.TempPlayer.jumped=False
   def test_jumping_acceleration(self):
      self.TempPlayer.jumpArc()
      #check if player is jumped get set to false when direction.y==0
      self.assertEqual(self.TempPlayer.jumped,False)
      self.TempPlayer.direction.y=-5
      #testing if the grabity acceleration changes 
      self.TempPlayer.jumpArc()
      self.assertEqual(self.TempPlayer.direction.y,-5+1/15)
      self.TempPlayer.direction.y=0
   def test_update(self):
      tempBlock = block.Block(gs.blockSize, (8, 7), 0, gs.textureNames[gs.itemIDs[0]])
      tempGroup=pygame.sprite.Group()
      tempGroup.add(tempBlock)
      self.TempPlayer.jumped=True
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.jumped,False)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.y,1)
      for x in tempGroup:
         x.blockPosition=(8*gs.blockSize,10*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.y,0)
      self.TempPlayer.direction.x=-1
      for x in tempGroup:
         x.blockPosition=(7*gs.blockSize,8*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,0)
      self.TempPlayer.direction.x=-1
      for x in tempGroup:
         x.blockPosition=(7*gs.blockSize,9*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,0)
      self.TempPlayer.direction.x=1
      for x in tempGroup:
         x.blockPosition=(9*gs.blockSize,8*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,0)
      self.TempPlayer.direction.x=1
      for x in tempGroup:
         x.blockPosition=(9*gs.blockSize,9*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.x,0)
      self.TempPlayer.jumped=True
      for x in tempGroup:
         x.blockPosition=(8*gs.blockSize,8*gs.blockSize)
      self.TempPlayer.update(0,tempGroup)
      self.assertEqual(self.TempPlayer.direction.y,0)
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
      
unittest.main()
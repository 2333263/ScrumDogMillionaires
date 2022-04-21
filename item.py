#Item class to make implementation of inventory system easier
#Allows inventory to work with items that may not be Block objects
import gameSettings as gs
import pygame
class Item:
    def __init__(self, itemName, itemId):
        self.itemName = itemName
        self.itemId = itemId
        self.amount = 0
        self.texture=pygame.image.load(gs.textureNames[self.itemName])

    def getItemId(self):
        return self.itemId

    def increase(self):
        self.amount += 1

    def decrease(self):
        self.amount -= 1
    
    def getCount(self):
        return self.amount
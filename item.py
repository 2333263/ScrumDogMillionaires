#Item class to make implementation of inventory system easier
#Allows inventory to work with items that may not be Block objects
import gameSettings as gs
import pygame

class Item:
    '''def __init__(self, itemName, itemID):
        self.itemName = itemName
        self.itemID = itemID
        self.amount = 0
        self.texture=pygame.image.load(gs.textureNames[self.itemName])'''

    def __init__(self, *args):

        #When 2 args are given item(itemName, itemId)
        #Placeable item, blocks only (e.g. stone or bed)
        if len(args) == 2:
            self.itemName = args[0]
            self.itemID = args[1]
            self.isPlaceable = True
            self.hardness = 0
            self.amount = 0
            self.texture = pygame.image.load(gs.textureNames[self.itemName])
        #When 3 args are given item(itemName, itemId, hardness)
        #Non placeable item, tools or entity likes (e.g. piece of coal or wooden pickaxe)
        elif len(args) == 3:
            self.itemName = args[0]
            self.itemID = args[1]
            self.isPlaceable = False
            self.hardness = args[2]
            self.amount = 0
            self.texture = pygame.image.load(gs.textureNames[self.itemName])


    def getItemName(self):
        return self.itemName

    def getItemId(self):
        return self.itemID

    def increase(self):
        self.amount += 1

    def decrease(self):
        self.amount -= 1
    
    def getCount(self):
        return self.amount

    def getHardness(self): 
        return self.hardness
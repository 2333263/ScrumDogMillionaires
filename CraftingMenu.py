import pygame
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos, req
from CraftButtonHandler import Button 
from TextHandler import Text
from inventoryHandler import getInventoryItems
from item import Item
import recipeHandler as rh

class Crafting():
    def __init__(self, screen):
        self.recipies = rh.RecipeHandler()
        self.allItems = self.recipies.getAllItemIDs()
    
        self.screen = screen
        self.menuBackround = pygame.sprite.Group()

        self.leftArrow = Text("<", 35, "white",  ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2.5, craftingTablePos[1] - blockSize * 5.5))
        self.rightArrow = Text(">", 35, "white", ((craftingTablePos[0] + blockSize/2) + (blockSize * 5)/3, craftingTablePos[1] - blockSize * 5.5))
        
        self.menuBackround.add(Button(9, ((craftingTablePos[0] + blockSize/2) - (blockSize * 5)/2, craftingTablePos[1] - blockSize * 10), blockSize * 5, blockSize * 10))
        self.menuBackround.add(self.leftArrow)
        self.menuBackround.add(self.rightArrow)
       

import pygame
from gameSettings import itemIDs, textureNames, blockSize, craftingTablePos
from CraftButtonHandler import Button 
from TextHandler import Text
from item import Item
import recipeHandler as rh

class Crafting():
    def __init__(self, screen):
        self.recipies = rh.RecipeHandler()
        self.allItems = self.recipies.getAllItemIDs()
        self.screen = screen
        self.menuBackround = self.makeBackground()

        
       
    def makeScreen(self):
        self.menuBackround.draw(self.screen)

    def makeBackground(self):
        tempBackround = pygame.sprite.Group()
        leftArrow = Text("<", 35, "white",  (craftingTablePos[0] - blockSize * 3.5, craftingTablePos[1] - blockSize * 5.5/2))
        rightArrow = Text(">", 35, "white",  (craftingTablePos[0] + blockSize * 4.5, craftingTablePos[1] - blockSize * 5.5/2))

        tempBackround.add(Button(9, (craftingTablePos[0] - blockSize * 4.5, craftingTablePos[1] - blockSize * 5.5), blockSize * 10, blockSize * 5))
        tempBackround.add(leftArrow)
        tempBackround.add(rightArrow)
        return tempBackround
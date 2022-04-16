import pygame
import pygame_gui
import gameSettings as gs
from levelGenerator import getBlocks

def createButton(manager, buttonText, size, position):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, size), text=buttonText, manager=manager)


def createCraftingList(craftableItemsArray, manager):
    count = 1
    for item in craftableItemsArray:
        createButton(manager, item, (100, 25), (gs.craftingPos[0] - 35, (gs.craftingPos[1] - 20) * count/4))
        count+=1
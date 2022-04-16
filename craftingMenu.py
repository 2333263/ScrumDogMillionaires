import pygame
import pygame_gui

def createButton(manager, buttonText, size, position):
    return pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, size), text=buttonText, manager=manager)
import pygame
import gameSettings as gs

portal = pygame.image.load(gs.textureNames["Portal"]) #load image for information screen
portal = pygame.transform.scale(portal, (0.5, 0.5)) #fit to page

def CheckEndGame(pos, screen):
    if(gs.endGamePos[0] != -1):
        if(pos == gs.endGamePos):
            #Draw the portal
            screen.blit(portal, pos)

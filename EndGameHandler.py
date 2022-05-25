import pygame
import gameSettings as gs

def CheckEndGame(screen, portal, ):
    if(gs.endGamePos[0] != -1):
        #Draw the portal
        screen.blit(portal, gs.endGamePoss)
        

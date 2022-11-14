import pygame
from MainGame.Items import itemHandler as ih

itemIDs = ih.fetchItemIDs()
textureNames = ih.fetchTextureNames()


class Button(pygame.sprite.Sprite):
    def __init__(self, itemID, pos, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.itemID = itemID
        self.pos = pos

        self.image = pygame.image.load(textureNames[itemIDs[itemID]]) #image to use on the button
        self.image = pygame.transform.scale(self.image, (width, height)) #scale the image for the button

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        

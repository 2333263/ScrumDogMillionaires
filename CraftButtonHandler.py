import pygame
from gameSettings import itemIDs, textureNames
class Button(pygame.sprite.Sprite):
    def __init__(self, itemID, pos, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.itemID = itemID
        self.pos = pos

        self.image = pygame.image.load(textureNames[itemIDs[itemID]]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        
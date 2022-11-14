import pygame

#A class for each slot in the inventory
#A slot is a rectangle in the main inventory rectangles and houses an item/block in the players inventory
class slot(pygame.sprite.Sprite):#class to represent the individual slots in the inventory
    def __init__(self, colour,left,top,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([width,height])
        self.image.fill(colour)
        self.width=width
        self.height=height
        self.rect=self.image.get_rect()
        self.rect.x=left
        self.rect.y=top

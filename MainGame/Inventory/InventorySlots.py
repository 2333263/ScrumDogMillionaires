import pygame


class slot(pygame.sprite.Sprite):
    def __init__(self, colour,left,top,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([width,height])
        self.image.fill(colour)
        self.width=width
        self.height=height
        self.rect=self.image.get_rect()
        self.rect.x=left
        self.rect.y=top

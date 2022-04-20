import pygame
import gameSettings as gs

#create camera class
class Camera(pygame.sprite.Group):
    def __init__(self,player):
        super().__init__(
        self.offset=pygame.math.Vector2()
        self.hWidth=gs.width/2
        self.hHeight=gs.height/2
        self.Player=player
#this function calculates the offset of the camera
    def scroll(self):
        #if(self.Player.rect.x<2):
        #    self.offset.x=0
        #else:
        self.offset.x=self.Player.rect.centerx-self.hWidth
        self.offset.y=self.Player.rect.centery-self.hHeight
    #this function takles in all blocks and the screen
    #offsets the position of the blocks and blits them
    #also offsets the players position and blits it
    def draw(self, screen, worldBlocks):
        self.scroll()
        for i in worldBlocks:
            screen.blit(i.image,(i.rect.x-self.offset.x,i.rect.y-self.offset.y))
        screen.blit(self.Player.image, (self.Player.rect.x-self.offset.x, self.Player.rect.y-self.offset.y))
#returns the offset
    def getOffsets(self):
        self.scroll()
        return self.offset
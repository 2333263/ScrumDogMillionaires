import pygame
import gameSettings as gs


#create camera class
class Camera(pygame.sprite.Group):
    def __init__(self,player):
        super().__init__()
        self.offset=pygame.math.Vector2()
        self.hWidth=gs.width/2
        self.hHeight=gs.height/2
        self.Player=player
      
       

#this function calculates the offset of the camera
    def scroll(self):
      # if(self.Player.rect.centerx-self.hWidth<=0):
       #    self.offset.x=0
       #elif(self.Player.rect.centerx-self.hWidth>=gs.width-gs.blockSize*32) : 
      #      self.offset.x=gs.width-gs.blockSize*32
      # else:
          
       self.offset.x=self.Player.rect.centerx-self.hWidth
       self.offset.y=self.Player.rect.centery-self.hHeight
    #this function takles in all blocks and the screen
    #off the position of the blocks and blits them
    #also offsets the players position and blits it
    def draw(self, screen, worldBlocks):
        self.scroll()
        collideabeBlocks=[] #list of blocks player can collide with, done here so that we only loop through the block array once per time step
        #mousePos = pygame.mouse.get_pos()
        for i in worldBlocks:
            if(self.isColideable(i)):
                collideabeBlocks.append(i)
            if(self.isOnScreen(i)):
                screen.blit(i.image,(i.rect.x-self.offset.x,i.rect.y-self.offset.y))

           
        screen.blit(self.Player.image, (self.Player.rect.x-self.offset.x, self.Player.rect.y-self.offset.y))
        return collideabeBlocks
    
#returns the offset
    def getOffsets(self):
        self.scroll()
        return self.offset

    def isColideable(self, block): #checks if block is close enough to player for them to be able to collide with them to not waste compute time on the collison calculations on far away blocks
        if(abs(block.rect.x-self.Player.rect.x)/gs.blockSize<=2):
            if(abs(block.rect.y-self.Player.rect.y)/gs.blockSize<=2):
                return True
        return False
    def isOnScreen(self,block): #checks if block is close enough to player to be visible on screen to save compute time by not drawing objects that are outside the viewable window
        if(abs(block.rect.x-self.Player.rect.x)/gs.blockSize<=gs.CHUNK_SIZE[0]/1.5):
            if(abs(block.rect.y-self.Player.rect.y)/gs.blockSize<=gs.CHUNK_SIZE[0]/2):
                return True
        return False
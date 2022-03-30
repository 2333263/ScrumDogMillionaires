import pygame
#import pymunk
import game_settings as gs
import math


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,size,colour):
       super().__init__()
       pygame.sprite.Sprite.__init__(self)
       self.playerSize=size
       self.playerPos=pos
       self.playerColour=colour
       self.image=pygame.Surface((size,2*size))
       self.jumped=False
       self.rect = self.image.get_rect(topleft=pos)
       Image=pygame.image.load("sprite the knight 648 x 1296/IMG-4203.PNG")
       Image=pygame.transform.scale(Image,(size,2*size))
       self.image=Image
       self.direction=pygame.math.Vector2(0,0)
       self.gravity=1
       self.character=Image

    def updatePlayerPos(self,pos):
        self.playerPos=pos


    
        
    def MoveOnX(self):
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            self.image=pygame.transform.flip(self.character,True, False)
            self.direction.x=-1
            
        if(keys[pygame.K_RIGHT]):
            self.image=self.character
            self.direction.x=1
    def use_gravity(self):
        self.direction.y=self.gravity
    def jump(self):
        if(self.direction.y==0):

            self.direction.y=-3
            self.jumped=True
    def jumpArc(self):
        self.direction.y+=self.gravity/20
        if(self.direction.y>=0):
    
            self.jumped=False
            
    def update(self, allBlocks):
        if(self.jumped==True):
            self.jumpArc()
        else:
            self.use_gravity()

        self.findCollision(allBlocks)
        
        
        self.rect.x+=self.direction.x
        self.rect.y += self.direction.y
    def StopMoveOnX(self):
        self.direction.x=0
    def findCollision(self,allBlocks):
        for block in allBlocks:
            if(not self.jumped and math.floor((self.rect.y+2*gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size):
                if(math.floor(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size or math.ceil(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size) :
                    self.direction.y=0  #blocks below
            elif(self.rect.x<0 and self.direction.x<0 or self.rect.x+gs.block_size>gs.width and self.direction.x>0): #world borders
                    self.direction.y=0
                    self.direction.x=0
            if(self.direction.x>0 and self.rect.x+gs.block_size==block.blockPosition[0] or self.direction.x<0 and self.rect.x==block.blockPosition[0]+gs.block_size):
                if(math.floor(self.rect.y/gs.block_size)==block.blockPosition[1]/gs.block_size or math.ceil(self.rect.y/gs.block_size)==block.blockPosition[1]/gs.block_size
                or math.floor((self.rect.y+gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size or math.ceil((self.rect.y+gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size):
                    self.direction.x=0 #blocks left and right

            if(self.jumped and math.ceil((self.rect.y)/gs.block_size)==(block.blockPosition[1]+gs.block_size)/gs.block_size):
                  if(math.floor(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size or math.ceil(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size) :
                    self.direction.y=0
                    self.jumped=False

          
                


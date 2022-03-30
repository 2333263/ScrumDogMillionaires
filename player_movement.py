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
       self.image.fill(colour)
       self.rect = self.image.get_rect(topleft=pos)
       self.direction=pygame.math.Vector2(0,0)
       self.gravity=1

    def updatePlayerPos(self,pos):
        self.playerPos=pos

    def MoveOnX(self):
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_LEFT]):
            self.direction.x=-1
        if(keys[pygame.K_RIGHT]):
            self.direction.x=+1
    def use_gravity(self):
        self.direction.y=self.gravity

    def update(self, allBlocks):
        self.use_gravity()
        self.findCollision(allBlocks)
        self.rect.x+=self.direction.x
        self.rect.y += self.direction.y
    def StopMoveOnX(self):
        self.direction.x=0
    def findCollision(self,allBlocks):
        for block in allBlocks:
            if(self.rect.y+2*gs.block_size==block.blockPosition[1]):
                if(math.floor(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size or math.ceil(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size) :
                    self.direction.y=0
            elif(self.rect.x<0 and self.direction.x<0 or self.rect.x+gs.block_size>gs.width and self.direction.x>0): #world borders
                    self.direction.y=0
                    self.direction.x=0
            if(self.direction.x>0 and self.rect.x+gs.block_size==block.blockPosition[0] or self.direction.x<0 and self.rect.x==block.blockPosition[0]+gs.block_size):
                if(math.floor(self.rect.y/gs.block_size)==block.blockPosition[1]/gs.block_size or math.ceil(self.rect.y/gs.block_size)==block.blockPosition[1]/gs.block_size
                or math.floor((self.rect.y+gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size or math.ceil((self.rect.y+gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size):
                    self.direction.x=0
          
                


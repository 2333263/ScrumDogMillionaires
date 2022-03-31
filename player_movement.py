import pygame
#import pymunk
import game_settings as gs
import math

# defintes a class player with several attributes
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,size):
       super().__init__()
       pygame.sprite.Sprite.__init__(self)
       self.playerSize=size
       self.playerPos=pos
       #create a surface of size (seize and 2 size)
       self.image=pygame.Surface((size,2*size))
       self.jumped=False
       #create a rect based on the size of the surface
       self.rect = self.image.get_rect(topleft=pos)
       #loads the sprite from the file
       Image=pygame.image.load("sprite the knight 648 x 1296/IMG-4203.PNG")
       Image=pygame.transform.scale(Image,(size,2*size))
       #swap the sprite drawn from the surface to the image
       self.image=Image
       #declare a change in direction vector
       self.direction=pygame.math.Vector2(0,0)
       self.gravity=1
       #save a copy of the sprite for later
       self.character=Image


    #updates the player position based on the current pos, this is not longer used
    def updatePlayerPos(self,pos):
        self.playerPos=pos



    def MoveOnX(self):
        #gets a list of all keys currently being pressed
        keys=pygame.key.get_pressed()
        #if the left arrow is being pressed
        if(keys[pygame.K_LEFT] or keys[pygame.K_a]):
            #flip the sprite so its facing left
            self.image=pygame.transform.flip(self.character,True, False)
            #set the change in directions vector to -1 in position x
            self.direction.x=-1
        #if the right arrow is being pressed
        if(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            #set the sprite to be the direction of the original image
            self.image=self.character
            #set the change in directions vector to 1 in position x
            self.direction.x=1
        #if neither the left nor right arrow is being pressed
        if(not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_d] and not keys[pygame.K_a]):
            #run the stop Move on X method which sets the direction vector as position x to 0
            self.StopMoveOnX()
        #sets the change in direction vector to the same as gravity in the y position
    def use_gravity(self):
        self.direction.y=self.gravity

    def jump(self):
        #if the player is not moving in the y direction
        if(self.direction.y==0):
            #set the change of direction to -3 in the y direction (ie go up by 3 places)
            self.direction.y=-3
            #set jump to true
            self.jumped=True

    def jumpArc(self):
        #add 1/15th of gravity to the current change in direction (this causes an arc when jumping)
        self.direction.y+=self.gravity/15
        #when the player reaches his arc set jumped to false so normal gravity functions
        if(self.direction.y>=0):
    
            self.jumped=False
            
    def update(self, allBlocks):
        #if the player is jumping use the jump arc gravity instead of normal gravity
        if(self.jumped==True):
            self.jumpArc()
        else:
            #otherwise use normal gravity
            self.use_gravity()
        #check if there are any collisions
        self.findCollision(allBlocks)
        
        #change the position of the player based on the values in the change direction vector
        self.rect.x+=self.direction.x
        self.rect.y += self.direction.y
    def StopMoveOnX(self):
        self.direction.x=0
    def findCollision(self,allBlocks):
        #loop through all blocks
        for block in allBlocks:
            #this bit checks to see if the player is standing on any blocks, we use floor and ceiling to ensure that it works even if the player is between 2 blocks, but only if theyre not jumping
            if(not self.jumped and math.floor((self.rect.y+2*gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size):
                if(math.floor(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size or math.ceil(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size) :
                    self.direction.y=0  #blocks below
                #checks to see if theyre at a world border
            elif(self.rect.x<0 and self.direction.x<0 or self.rect.x+gs.block_size>gs.width and self.direction.x>0): #world borders
                    self.direction.y=0
                    self.direction.x=0
            #checks to see if there are any collisions to the left or right of the player
            if(self.direction.x>0 and self.rect.x+gs.block_size==block.blockPosition[0] or self.direction.x<0 and self.rect.x==block.blockPosition[0]+gs.block_size):
                if(math.floor(self.rect.y/gs.block_size)==block.blockPosition[1]/gs.block_size or math.ceil(self.rect.y/gs.block_size)==block.blockPosition[1]/gs.block_size
                or math.floor((self.rect.y+gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size or math.ceil((self.rect.y+gs.block_size)/gs.block_size)==block.blockPosition[1]/gs.block_size):
                    self.direction.x=0 #blocks left and right
            #same as first if, but its the blocks above the player when they jump
            if(self.jumped and math.ceil((self.rect.y)/gs.block_size)==(block.blockPosition[1]+gs.block_size)/gs.block_size):
                  if(math.floor(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size or math.ceil(self.rect.x/gs.block_size)==block.blockPosition[0]/gs.block_size) :
                    self.direction.y=0
                    self.jumped=False

          
                


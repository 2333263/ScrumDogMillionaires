import pygame
import gameSettings as gs
import math

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        #Any reference to playerPos or player.pos is deprecated, please use player.getPlayerPos() instead. This returns a tuple of x and y coordinates.
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.playerSize=size
        #create a surface of size (seize and 2 size)
        self.image=pygame.Surface((size,2*size))
        self.jumped=False
        #create a rect based on the size of the surface
        self.rect = self.image.get_rect(topleft=pos)
        #loads the sprite from the file
        Image=pygame.image.load("Textures/Player/sprite.png")
        Image=pygame.transform.scale(Image,(size,2*size))
        #swap the sprite drawn from the surface to the image
        self.image=Image
        #declare a change in direction vector
        self.direction=pygame.math.Vector2(0.0,0.0)
        self.gravity = 1
        #save a copy of the sprite for later
        self.character=Image

    def getPlayerPos(self):
        return self.rect.x, self.rect.y

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
            #set the change in directions vector to -2 in position x
            self.direction.x=-2
        #if the right arrow is being pressed
        if(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            #set the sprite to be the direction of the original image
            self.image=self.character
            #set the change in directions vector to 2 in position x
            self.direction.x=2
        #if neither the left nor right arrow is being pressed
        if(not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_d] and not keys[pygame.K_a]):
            #run the stop Move on X method which sets the direction vector as position x to 0
            self.stopMoveOnX()
        
    #sets the change in direction vector to the same as gravity in the y position
    def useGravity(self):
        self.direction.y=self.gravity

    def jump(self):
        #if the player is not moving in the y direction
        if(self.direction.y==0):
            #set the change of direction to -3 in the y direction (ie go up by 3 places)
            self.direction.y=-2
            #set jump to true
            self.jumped=True

    def jumpArc(self):
        #add 1/15th of gravity to the current change in direction (this causes an arc when jumping)
        self.direction.y+=self.gravity/15
        #when the player reaches his arc set jumped to false so normal gravity functions
        if(math.floor(self.direction.y)==0):
            self.jumped=False


    def update(self, dt, allBlocks):
        #if the player is jumping use the jump arc gravity instead of normal gravity
        if(self.jumped==True):
            self.jumpArc()
        else:
            #otherwise use normal gravity
            self.useGravity()
        # #check if there are any collisions

        collided_block = pygame.sprite.spritecollideany(self, allBlocks, collided = None)

        # if(collision != None):
        #     self.handleCollision(collision)
    
        if(collided_block != None):
            if (self.direction.x < 0 and collided_block.rect.x < self.rect.x): #left
                self.direction.x = 0
            elif (self.direction.x >= 0 and collided_block.rect.x > self.rect.x): #right
                self.direction.x = 0
        

            if (self.direction.y > 0 and collided_block.rect.top - gs.blockSize < self.rect.y ): #up
                self.direction.y = 0
            elif (self.direction.y < 0 and collided_block.rect.top >= self.rect.bottom): #down
                self.direction.y = 0
       
        if(dt>0):
            self.rect.x += self.direction.x * dt
            self.rect.y += self.direction.y * dt
        else:
            self.rect.x += self.direction.x 
            self.rect.y += self.direction.y 
        

    def stopMoveOnX(self):
        self.direction.x=0

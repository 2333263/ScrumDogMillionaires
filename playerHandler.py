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
        self.gravity = 2
        #save a copy of the sprite for later
        self.character=Image
        self.y_momentum=0
        self.keys={}

    def getPlayerPos(self):
        return self.rect.x, self.rect.y


    def MoveOnX(self,fakeKeys):
        #gets a list of all keys currently being pressed
        if(len(fakeKeys)==0):
            self.keys=pygame.key.get_pressed()
        else:
            self.keys=fakeKeys
        #if the left arrow is being pressed
        if(self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]):
            #flip the sprite so its facing left
            self.image=pygame.transform.flip(self.character,True, False)
            #set the change in directions vector to -2 in position x
            self.direction.x=-2
        #if the right arrow is being pressed
        if(self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]):
            #set the sprite to be the direction of the original image
            self.image=self.character
            #set the change in directions vector to 2 in position x
            self.direction.x=2
        #if neither the left nor right arrow is being pressed
        if(not self.keys[pygame.K_RIGHT] and not self.keys[pygame.K_LEFT] and not self.keys[pygame.K_d] and not self.keys[pygame.K_a]):
            #run the stop Move on X method which sets the direction vector as position x to 0
            self.stopMoveOnX()
        
    #sets the change in direction vector to the same as gravity in the y position
    def useGravity(self):
        self.direction.y=self.gravity

    def jump(self):
        #if the player is not moving in the y direction
        if(self.direction.y==0):
            #set the change of direction to -3 in the y direction (ie go up by 3 places)
            self.direction.y=-2.5
            #set jump to true
            self.jumped=True

    def jumpArc(self):
        #add 1/15th of gravity to the current change in direction (this causes an arc when jumping)
        self.direction.y+=self.gravity/20
        #when the player reaches his arc set jumped to false so normal gravity functions
        if(math.floor(self.direction.y)==0):
            self.jumped=False
            
    def collided(self,blocks):
        collide_list=[]
        for block in blocks: #checks all nearby blocks
            if self.rect.colliderect(block): #uses sprite grpup collide
                 collide_list.append(block)
        return   collide_list
        

    def update(self, dt, blocks):
        #if the player is jumping use the jump arc gravity instead of normal gravity
        if(self.jumped==True):
            self.jumpArc()
        else:
            #otherwise use normal gravity
            self.useGravity()
      #shift rect to moved pos on x
        if(dt>0):
            self.rect.x += self.direction.x * dt
        else:
            self.rect.x+=self.direction.x
        #gets a list of blocks that collide with player sprite
        collide_list=self.collided(blocks)

        for block in collide_list:
                if self.direction.x>0: # if moving right
                    self.rect.right=block.rect.left #collide with block on right
                    self.direction.x=0 #no movement on x
                    
                    
                elif self.direction.x<0:# if moving left
                    self.rect.left=block.rect.right #collide with block on left
                    self.direction.x=0 #no movement on x
        #shift rect to moved pos on y
        if(dt>0):
            self.rect.y += self.direction.y * dt
        else:
            self.rect.y+=self.direction.y
        #gets a list of blocks that collide with plater sprite
        collide_list=self.collided(blocks)
        for block in collide_list:
                if self.direction.y>0:  # if moving down
                    self.rect.bottom=block.rect.top #collide with block on bottom
                    self.direction.y=0 #no movement on y
                elif self.direction.y<0: # if moving up
                    self.rect.top=block.rect.bottom #collide with block on top
                    self.direction.y=0 #no movement on y
                    self.jumped=False #no longer jumping

    def stopMoveOnX(self):
        self.direction.x=0

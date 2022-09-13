from math import ceil
from tarfile import BLOCKSIZE
import pygame
import sys
sys.path.append("../Scrum-Dog-Millionaires")
import gameSettings as gs
from ChunkGenerator import generateChunk
import playerHandler as ph
import Camera as cam
import inventoryHandler
import breakPlaceHandler as bph
import random

class MinePy:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((gs.width, gs.height))
        #self.screen = pygame.Surface((gs.width, gs.height))
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        #self.mode = 0
        self.player = ph.Player(((gs.width/2 - gs.blockSize * 4)+0.5*gs.blockSize, - gs.blockSize*2), gs.blockSize)
        self.camera = cam.Camera(self.player)
        self.worldBlocks = pygame.sprite.Group()
        self.collisionblocks = self.worldBlocks 
        gs.generatedChunks[0] = generateChunk(0, self.worldBlocks)
        self.offset=[[0,0], [1,-1], [2,-1],
                    [0,0], [0,1], [2,0], [2, 1],
                    [0,2], [1, 2], [2, 2]] 
   
    def action(self, action):
        #print(self.player.getPlayerPos())
        if action == gs.actionSpace["MOVEMENT"][2]:
            self.player.jump()
        elif action in gs.actionSpace["MOVEMENT"][1:]:
            self.player.MoveOnX({}, action)
        elif action in gs.actionSpace["WORLD"]:
            if action in gs.actionSpace["WORLD"][0:10]:
                realAction = action - gs.actionSpace["WORLD"][0]
            else: 
                realAction = action - gs.actionSpace["WORLD"][10]
            playerPos=self.player.getPlayerPos()
            lst=list(playerPos)
            lst[0]+=self.offset[realAction][0] * gs.blockSize
            lst[1]+=self.offset[realAction][1] * gs.blockSize
            playerPos=tuple(lst)

            if action in gs.actionSpace["WORLD"][0:10]:
                bph.blockBreak(playerPos, self.worldBlocks, self.player,False, False)
            else:
                bph.blockPlace(playerPos, self.worldBlocks, self.player,False, False)
            
        elif action in gs.actionSpace["HOTBAR"]:
            inventoryHandler.selectInventory(action - gs.actionSpace["HOTBAR"][0])


        self.player.update(self.clock.tick(), self.worldBlocks)  #may need to change to collison blocks later
        #print(self.player.getPlayerPos())

    def evaluate(self):      
        return 0    

    def is_done(self):
        return False               
    
    def observe(self):
        #RGB array?? --> views
        return self.player.getPlayerPos()

    #Should be RGB array in future? 
    def view(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                quit()

        #DO drawing 
        bg = pygame.Rect(0, 0, gs.width, gs.height)
        pygame.draw.rect(self.screen, (0, 0, 0), bg)
        self.collisionblocks = self.camera.draw(self.screen, self.worldBlocks)
        inventoryHandler.drawHotBar(self.screen) #--> draw inventory 
        #pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.game_speed)



    
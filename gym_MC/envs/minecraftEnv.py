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
from CraftingMenu import Crafting

class MinePy:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((gs.width, gs.height))
        #self.screen = pygame.Surface((gs.width, gs.height))
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        #self.mode = 0
        self.player = ph.Player(((gs.width/2 - gs.blockSize * 4)+0.75*gs.blockSize, - gs.blockSize*2), gs.blockSize)
        self.camera = cam.Camera(self.player)
        self.worldBlocks = pygame.sprite.Group()
        self.collisionblocks = self.worldBlocks 
        self.crafter = Crafting(self.screen)
        gs.generatedChunks[0] = generateChunk(0, self.worldBlocks)
        self.offset=[[-1,-1], [0,-1], [1,-1], #offsets of player positions, top row is above player
                    [-1,0], [-1,1], [1,0], [1, 1], #left down, left up, right down, right up
                    [-1,2], [0, 2], [1, 2]] #below the player
   
    def action(self, action):
        if action == gs.actionSpace["MOVEMENT"][2]:
            self.player.jump()
        elif action in gs.actionSpace["MOVEMENT"][1:]:
            self.player.MoveOnX({}, action)
        elif action in gs.actionSpace["WORLD"]:
            if action in gs.actionSpace["WORLD"][0:10]:
                realAction = action - gs.actionSpace["WORLD"][0]
            else: 
                realAction = action - gs.actionSpace["WORLD"][10]
            playerPos=[self.player.getPlayerPos()[0],self.player.getPlayerPos()[1]]
            playerPos[0]+=self.offset[realAction][0] * gs.blockSize
            playerPos[1]+=self.offset[realAction][1] * gs.blockSize

            if action in gs.actionSpace["WORLD"][0:10]:
                bph.blockBreak(playerPos, self.worldBlocks, self.player,False, False)
            else:
                bph.blockPlace(playerPos, self.worldBlocks, self.player,False, False)
            
        elif action in gs.actionSpace["HOTBAR"]:
            inventoryHandler.selectInventory(action - gs.actionSpace["HOTBAR"][0])

        elif action in gs.actionSpace["CRAFTING"]:
            craftingID = action - gs.actionSpace["CRAFTING"][0]
            craftPossibility = self.crafter.craftSpec(craftingID, inventoryHandler.getInv())


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



    
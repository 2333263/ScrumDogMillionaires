from math import ceil
from tarfile import BLOCKSIZE
import pygame
import sys
sys.path.append("../Scrum-Dog-Millionaires")
import gameSettings as gs
from ChunkGenerator import generateChunk
import playerHandler as ph
import Camera as cam
import inventoryHandler as inv
import breakPlaceHandler as bph
from CraftingMenu import Crafting

class MinePy:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((gs.width, gs.height))
        #self.screen = pygame.Surface((gs.width, gs.height))
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        self.stage = 1
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
    

    [-1, 0, 1, 2, 3, 4]
    def action(self, action):
        if action == gs.actionSpace["MOVEMENT"][2]:
            self.player.jump()
        elif action in gs.actionSpace["MOVEMENT"][1:3]:
            self.player.MoveOnX({}, action)
            
        elif action == gs.actionSpace["MOVEMENT"][4]:
            self.player.jump()
            self.player.MoveOnX({}, gs.actionSpace["MOVEMENT"][1])

        elif action == gs.actionSpace["MOVEMENT"][5]:
            self.player.jump()
            self.player.MoveOnX({}, gs.actionSpace["MOVEMENT"][3])

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
            inv.selectInventory(action - gs.actionSpace["HOTBAR"][0])

        elif action in gs.actionSpace["CRAFTING"]:
            craftingID = action - gs.actionSpace["CRAFTING"][0]
            craftPossibility = self.crafter.craftSpec(craftingID, inv.getInv())


        self.player.update(self.clock.tick(), self.worldBlocks)  #may need to change to collison blocks later
        #print(self.player.getPlayerPos())

    def evaluate(self, prev): 
        current = inv.getInv()
        
        if self.stage == 1: #collect logs
            stageRewards = {7 : 10, 6 : 2, 1 : 1, 0 : 3} #itemID : reward
            for key in stageRewards.keys:
                prevCount = inv.getItemCountFromInput(key, prev)
                currCount = inv.getItemCountFromInput(key, current)
                
                if currCount == 4 and key == 7: # Complete stage 1
                    self.stage += 1
                    break

                if prevCount < currCount: # if broke blocks
                    return stageRewards[key]

                if prevCount > currCount and key == 7: # If place wood logs
                    return -5
                
                return 0.01 #any other actions
            
        if self.stage == 2: #craft wooden planks
            # Does not have enough planks and no more logs can craft -> move back to previous stage 
            if inv.getItemCountFromInput(7, current) == 0 and inv.getItemCountFromInput(8, current) < 8 :
                self.stage -= 1
            
            #has enough planks to craft a pickaxe -> move to next stage
            elif inv.getItemCountFromInput(8, current) >= 8:
                self.stage += 1
            
            planksPrevCount = inv.getItemCountFromInput(8, prev)
            planksCurrCount = inv.getItemCountFromInput(8, current)
            logsPrevCount = inv.getItemCountFromInput(7, prev)
            logsCurrCount = inv.getItemCountFromInput(7, current)
            
            if logsPrevCount > logsCurrCount: # less logs than before
                if planksPrevCount < planksCurrCount:
                    return 10
                return -10
            
            return 0.01 #any other actions

        return 0
            

    def is_done(self):
        return False               
    
    def observe(self):
        #RGB array?? --> views
        return inv.getInv()

    #Should be RGB array in future? 
    def view(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                quit()

        #DO drawing 
        bg = pygame.Rect(0, 0, gs.width, gs.height)
        pygame.draw.rect(self.screen, (0, 0, 0), bg)
        self.collisionblocks = self.camera.draw(self.screen, self.worldBlocks)
        inv.drawHotBar(self.screen) #--> draw inventory 
        #pygame.display.update()
        pygame.display.flip()
        self.clock.tick(self.game_speed)



    
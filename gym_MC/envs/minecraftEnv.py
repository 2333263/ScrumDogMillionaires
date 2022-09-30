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
from itemNew import Item
import itemHandler as ih
from block import Block
itemIDs = ih.fetchItemIDs()
items = ih.fetchDict()

class MinePy:
    
    metadata = {"render_modes" : ["human","rgb_array"], "render_fps": 64}
    #if render mode is human, render game to screen- if it is None- render game to surface
    #if seed is empty, random seed is used, else hash of seed is used.
    
    def __init__(self,render_mode="human", seed="", easyStart=2,playerRange=7): 
        pygame.init()
        for i in items:
            if(i.amount>0):
                i.amount=0
        self.render_mode=render_mode
        if(render_mode=="rgb_array"):
            #if render mode is rgb_array do not render game to screen, render to surface
            self.screen = pygame.Surface((gs.width, gs.height))
        elif(render_mode=="human"):
            #if render mode is human render game to the screen
            self.screen = pygame.display.set_mode((gs.width, gs.height))
        
        #there are three levels for easyStart:
        #level 0: empty inventory
        #level 1: wooden pickaxe, 4 wooden planks
        if(easyStart==1):
            newTempItem = items[12]
            inv.addItem(newTempItem)
            tempBlock = items[9]
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
        #level 2: wooden pickaxe, 4 wooden planks, a stone pickaxe and a diamond, and an emerald!
        #really easy start
        if(easyStart==2):
            #newTempItem = Item("Wooden Pickaxe",11, 0)
            newTempItem = items[12]
            inv.addItem(newTempItem)
            #newTempItem2 = Item("Diamond",50, 0)
            newTempItem2 = items[51]
            inv.addItem(newTempItem2)
            #tempBlock=Item(itemIDs[8],8)
            tempBlock = items[9]
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            #newTempItem3 = Item("Stone Pickaxe",16, 0)
            newTempItem3 = items[17]
            inv.addItem(newTempItem3)
            #newTempItem4 = Item("Emerald" ,53, 0)
            newTempItem4 = items[54]
            inv.addItem(newTempItem4)
            
        self.clock = pygame.time.Clock()
        self.game_speed = 60
        self.stage = 1
        self.done = False
        #set the seed
        gs.seed=gs.setSeed(seed)
        #set the player range for breaking and placing blocks, clicking on items
        gs.playerRange=playerRange
        # print("gs.playerRange is=", gs.playerRange)
        # print("gs.seed is=", gs.seed)
        self.player = ph.Player(((gs.width/2 - gs.blockSize * 4)+0.75*gs.blockSize, - gs.blockSize*30), gs.blockSize)
        self.camera = cam.Camera(self.player)
        self.worldBlocks = pygame.sprite.Group()
        self.collisionblocks = self.worldBlocks 
        self.crafter = Crafting(self.screen)
        gs.generatedChunks[0] = generateChunk(0, self.worldBlocks)
        self.offset=[[-1,-1], [0,-1], [1,-1], #offsets of player positions, top row is above player
                    [-1,0], [-1,1], [1,0], [1, 1], #left down, left up, right down, right up
                    [-1,2], [0, 2], [1, 2]] #below the player
    
    
  
    
    def action(self, action):
        fakeKeys={pygame.K_LEFT:False,pygame.K_RIGHT:False,pygame.K_UP:False,pygame.K_a:False,pygame.K_d:False,pygame.K_w:False,pygame.K_SPACE:False}
        if action == gs.actionSpace["MOVEMENT"][2]:
            self.player.jump()
        elif action == gs.actionSpace["MOVEMENT"][1]:
            fakeKeys[pygame.K_LEFT]=True
            #self.player.MoveOnX(fakeKeys, action)
            self.player.MoveOnX(fakeKeys)
        elif action == gs.actionSpace["MOVEMENT"][3]:
            fakeKeys[pygame.K_RIGHT]=True
            #self.player.MoveOnX(fakeKeys, action)
            self.player.MoveOnX(fakeKeys)
        elif action == gs.actionSpace["MOVEMENT"][4]:
            self.player.jump()
            fakeKeys[pygame.K_LEFT]=True
            #self.player.MoveOnX(fakeKeys, gs.actionSpace["MOVEMENT"][1])
            self.player.MoveOnX(fakeKeys)
        elif action == gs.actionSpace["MOVEMENT"][5]:
            self.player.jump()
            fakeKeys[pygame.K_RIGHT]=True
            self.player.MoveOnX(fakeKeys)

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

        #print("In stage: ", self.stage)
        
        if self.stage == 1: #collect logs
            # 8 = wooden planks is here because if we get sent back to stage 1 
            # we need incentive to break those planks to go back to stage 4 from stage 2
            stageRewards = {8 : 10, 7 : 10, 6 : 2, 1 : 1, 0 : 3} #itemID : reward
            
            if inv.getItemCountFromInput(7, current) >= 2: # Complete stage 1
                    self.stage += 1
                    return 10

            for key in stageRewards.keys():
                prevCount = inv.getItemCountFromInput(key, prev)
                currCount = inv.getItemCountFromInput(key, current)

                if prevCount < currCount: # if broke blocks
                    return stageRewards[key]

                if prevCount > currCount and key == 7: # If place wood logs
                    return -5
                

            return 0.01 #any other actions
        
        elif self.stage == 2: #craft wooden planks
            # Does not have enough planks and has no logs
            if inv.getItemCountFromInput(7, current) == 0 and inv.getItemCountFromInput(8, current) < 8:
                #has a pickaxe (from stage 4) and has more than 2 wooden planks
                if inv.getItemCountFromInput(8, current) >= 2 and inv.getItemCountFromInput(11, current) > 0:
                    self.stage = 4 #go to stage 4 and try get enough stone
                    return 10
                else: # go back to stage 1
                    self.stage -= 1
                    return -10

            # has enough planks to craft a pickaxe -> move to next stage
            elif inv.getItemCountFromInput(8, current) >= 8:
                self.stage += 1
                return 20
            
            planksPrevCount = inv.getItemCountFromInput(8, prev)
            planksCurrCount = inv.getItemCountFromInput(8, current)
            logsPrevCount = inv.getItemCountFromInput(7, prev)
            logsCurrCount = inv.getItemCountFromInput(7, current)

            if logsPrevCount > logsCurrCount: # less logs than before
                if planksPrevCount < planksCurrCount:
                    return 20
                return -20
            
            # if sent back to this stage and can break planks that were placed
            if planksPrevCount < planksCurrCount:
                return 15
            
            return 0.01 #any other actions

        elif self.stage == 3: #craft a wooden pickaxe
            # less than minimum planks to craft one pickaxe and doesn't have a pickaxe
            # go to previous stage
            if inv.getItemCountFromInput(8, current) < 5 and inv.getItemCountFromInput(11, current) == 0:
                self.stage -= 1
                return -30
            
            # has a wooden pickaxe --> move to next stage
            elif inv.getItemCountFromInput(11, current) >= 1:
                self.stage += 1
                return 30

            # need 5 wooden planks to make 1 pickaxe
            planksPrevCount = inv.getItemCountFromInput(8, prev)
            planksCurrCount = inv.getItemCountFromInput(8, current)
            pickPrevCount = inv.getItemCountFromInput(11, prev)
            pickCurrCount = inv.getItemCountFromInput(11, current)

            if planksPrevCount > planksCurrCount: #either placed or crafted using planks
                if pickPrevCount < pickCurrCount: # crafted a pickaxe
                    return 30
                return -30 # placed a plank

            return 0.01 # any other action
        
        elif self.stage == 4: # collect stone and wooden planks
            stageRewards = {2 : 40 , 8 : 40, 7 : 10, 6 : 2, 1 : 1, 0 : 3} # itemID : reward
            reward = 0
            # might need to reward the agent for selecting the pickaxe
            # if selected == wooden pickaxe 
            # return 10 for eg
            # so that the agent can learn to use the pickaxe to break blocks with a higher hardness
            if inv.getSelected().itemID == 11:
                reward += 10
            else:
                reward -= 10

            # has enough resources to move to the next stage
            if inv.getItemCountFromInput(2, current) >= 3 and inv.getItemCountFromInput(8, current) >= 2:
                self.stage += 1
                return 40

            # dont have enough planks to craft stone pickaxe
            elif inv.getItemCountFromInput(8, current) < 2:
                self.stage = 2
                return -40

            for key in stageRewards.keys():
                prevCount = inv.getItemCountFromInput(key, prev)
                currCount = inv.getItemCountFromInput(key, current)

                if prevCount < currCount: #break blocks
                    return stageRewards[key] + reward

                if prevCount > currCount: #place stone or planks
                    if key == 2 or 8:
                        return -30

                return 0.01 + reward #other actions
            
        elif self.stage == 5: #craft stone pickaxe
            # Have less than minimum stone or wood to craft one pickaxe, and dont have a stone pickaxe
            if inv.getItemCountFromInput(16, current) == 0 and (inv.getItemCountFromInput(2, current) < 3 or inv.getItemCountFromInput(8, current) < 2):
                self.stage -= 1 
                return -50

            #crafted a stone pickaxe and can move to next stage
            elif inv.getItemCountFromInput(16, current) >= 1:
                self.stage += 1
                return 50
            
            # need 3 stone and 2 planks to craft a stone pickaxe
            stonePrevCount = inv.getItemCountFromInput(2, prev)
            stoneCurrCount = inv.getItemCountFromInput(2, current)
            planksPrevCount = inv.getItemCountFromInput(8, prev)
            planksCurrCount = inv.getItemCountFromInput(8, current)
            pickPrevCount = inv.getItemCountFromInput(16, prev)
            pickCurrCount = inv.getItemCountFromInput(16, current)

            #either placed or crafted using stone or planks 
            if stonePrevCount > stoneCurrCount or planksPrevCount > planksCurrCount:
                if pickPrevCount < pickCurrCount: #crafted pickaxe
                    return 50
                return -30 # placed stone or planks
            
            return 0.01 # other actions
        
        elif self.stage == 6: # collect gold ores, diamond ores and emerald ore
            stageRewards = {46 : 60, 49 : 60, 78 : 60, 2 : 40 , 8 : 40, 7 : 10, 6 : 2, 1 : 1, 0 : 3} # itemID : reward
            reward = 0
            # if we have selected the stone pickaxe 
            # otherwise we can't get resources needed 
            if inv.getSelected().itemID == 16:
                reward += 40
            else:
                reward -= 40

            #if has enough resouces to move to next stage
            if inv.getItemCountFromInput(46, current) >= 36 and inv.getItemCountFromInput(49, current) >= 36 and inv.getItemCountFromInput(78, current) >= 1:
                self.stage += 1
                return 60

            for key in stageRewards.keys():
                prevCount = inv.getItemCountFromInput(key, prev)
                currCount = inv.getItemCountFromInput(key, current)

                if prevCount < currCount: #break blocks
                    return stageRewards[key] + reward
                
                if prevCount > currCount: #placed blocks
                    if key == 46 or 49 or 78:
                        return -60

                return 0.01 + reward #other actions

        elif self.stage == 7: #craft diamond, gold ingot and emerald
            enough = inv.getItemCountFromInput(50, current) >= 36 and inv.getItemCountFromInput(47, current) >= 36 and inv.getItemCountFromInput(53, current) >= 1
            #have enough resources to go to the next stage
            if enough:
                self.stage += 1
                return 70
            
            #must've placed the blocks we needed and havent crafted so need to get the blocks again
            elif not enough:
                if inv.getItemCountFromInput(46, current) == 0  and inv.getItemCountFromInput(49, current) == 0 and inv.getItemCountFromInput(78, current) == 0:
                    self.stage -= 1
                    return -70
            minerals = [[49,50],[46,47],[78,53]]#diamond ore, diamond, gold ore, gold, emerald ore, emerald
            for c in minerals:
                OrePrevCount = inv.getItemCountFromInput(c[0], prev)
                OreCurrCount = inv.getItemCountFromInput(c[0], current)
                PrevCount = inv.getItemCountFromInput(c[1], prev)
                CurrCount = inv.getItemCountFromInput(c[1], current)
                if OrePrevCount > OreCurrCount: # could've placed or crafted  ore
                    if PrevCount < CurrCount: # crafted a minerals
                        return 70
                    return -50 # placed the block
            
            return 0.01 #other actions

        elif self.stage == 8: #craft diamond, gold blocks
            enough = inv.getItemCountFromInput(64, current) >= 4 and inv.getItemCountFromInput(67, current) >= 4
            #have enough resources to go to the next stage
            if enough:
                self.stage += 1
                return 80

            elif not enough:
                if inv.getItemCountFromInput(50, current) < 9 and inv.getItemCountFromInput(47, current) < 9:
                    self.stage -= 1
                    return -80

            minerals = [[50,67],[47,64]]#diamond, diamond block, gold, gold block
            for c in minerals:
                PrevCount = inv.getItemCountFromInput(c[0], prev)
                CurrCount = inv.getItemCountFromInput(c[0], current)
                BlockPrevCount = inv.getItemCountFromInput(c[1], prev)
                BlockCurrCount = inv.getItemCountFromInput(c[1], current)
                if PrevCount > CurrCount: # could've placed or crafted mineral
                    if BlockPrevCount < BlockCurrCount: # crafted a mineral 
                        return 100
                    return -70 # placed the block (incase mineral becomes placable)
           
            return 0.01 # random action
        
        
        elif self.stage == 9: #craft the end game block
            #crafted the end game block
            if inv.getItemCountFromInput(83, current) > 0:
                self.done = True
                return 1000 #game done
            
            else: #don't have enough resorces to craft the end game block
                if inv.getItemCountFromInput(67, current) < 4 and inv.getItemCountFromInput(64, current) < 4 and inv.getItemCountFromInput(53, current) == 0:
                    self.stage -= 1
                    return -100
            
            diamondPrevCount = inv.getItemCountFromInput(67, prev)
            diamondCurrCount = inv.getItemCountFromInput(67, current)
            goldPrevCount = inv.getItemCountFromInput(64, prev)
            goldCurrCount = inv.getItemCountFromInput(64, current)
            emeraldPrevCount = inv.getItemCountFromInput(53, prev)
            emeraldCurrCount = inv.getItemCountFromInput(53, current)
            endGamePrevCount = inv.getItemCountFromInput(83, prev)
            endGameCurrCount = inv.getItemCountFromInput(83, current)

            if diamondPrevCount > diamondCurrCount or goldPrevCount > goldCurrCount or emeraldPrevCount > emeraldCurrCount:
                if endGamePrevCount < endGameCurrCount: #crafted end game block
                    return 1000
                return -100 # placed blocks

            return 0.01 #other actions           

    def is_done(self):
        if self.done:
            return True #game done
        else:
            return False              
    
    def observe(self):
        #RGB array?? --> views
        # our observations shouldn't be the inventory, inventory should be in info for new step function
        # obersvations returns an RGB array of the frame
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
        if(self.render_mode=="human"):
            pygame.display.flip()
        #else:
            #pygame.display.update()
        self.clock.tick(self.game_speed)



    
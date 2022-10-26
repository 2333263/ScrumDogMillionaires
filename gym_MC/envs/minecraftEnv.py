from asyncio.windows_events import NULL
import pygame
import sys
import numpy as np

sys.path.append("../Scrum-Dog-Millionaires")
from MainGame.Settings import gameSettings as gs
from MainGame.Chunks.ChunkGenerator import generateChunk
from MainGame.Player import playerHandler as ph
from MainGame.Camera import Camera as cam
from MainGame.Inventory import inventoryHandler as inv
from MainGame.Blocks import breakPlaceHandler as bph
from MainGame.Crafting.CraftingMenu import Crafting
from MainGame.Items import itemHandler as ih
from MainGame.Rewards import rewardsHandler as rw
from MainGame.Chunks.ChunkHandler import checkChunkUpdates
import copy

itemIDs = ih.fetchItemIDs()
items = ih.fetchDict()


class MinePy:
    metadata = {"render_modes": ["human","rgb_array"],"render_fps": 60,"easyStart":[0,1,2]}

    # if render mode is human, render game to screen- if it is None- render game to surface
    # if seed is empty, random seed is used, else hash of seed is used.

    def __init__(self, render_mode="human", easyStart=1, playerRange=7, seed=None):
        pygame.init()
        self.seed=seed
        for i in items:
            if(i.amount>0):
                i.amount=0
        self.render_mode = render_mode
        self.inv=inv
        #self.inv.initGroup()
        if (render_mode == "rgb_array"):
            # if render mode is rgb_array do not render game to screen, render to surface
            self.screen = pygame.Surface((gs.width,gs.height)) 
        elif (render_mode == "human"):
            # if render mode is human render game to the screen
            
            self.screen = pygame.display.set_mode((gs.width,gs.height))
       
        # there are three levels for easyStart:
        # level 0: empty inventory
        # level 1: wooden pickaxe, 4 wooden planks
        if (easyStart == 1):
            newTempItem = items[12]
            inv.addItem(newTempItem)
            tempBlock = items[9]
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
        # level 2: wooden pickaxe, 4 wooden planks, a stone pickaxe and a diamond, and an emerald!
        # really easy start
        if (easyStart == 2):
            # newTempItem = Item("Wooden Pickaxe",11, 0)
            newTempItem = items[12]
            inv.addItem(newTempItem)
            # newTempItem2 = Item("Diamond",50, 0)
            newTempItem2 = items[51]
            inv.addItem(newTempItem2)
            # tempBlock=Item(itemIDs[8],8)
            tempBlock = items[9]
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            inv.addBlock(tempBlock)
            # newTempItem3 = Item("Stone Pickaxe",16, 0)
            newTempItem3 = items[17]
            inv.addItem(newTempItem3)
            # newTempItem4 = Item("Emerald" ,53, 0)
            newTempItem4 = items[54]
            inv.addItem(newTempItem4)

        self.clock = pygame.time.Clock()
        self.game_speed = 60
        self.stage = 1
        self.done = False
        # set the seed

        if(self.seed == None):
            self.seed = gs.genRandomSeed()
        gs.seed=self.seed

        # set the player range for breaking and placing blocks, clicking on items
        gs.playerRange = playerRange
        self.worldBlocks = pygame.sprite.Group()
        self.collisionblocks = self.worldBlocks
        gs.generatedChunks[-1] = generateChunk(-gs.CHUNK_SIZE[0], self.worldBlocks)
        gs.generatedChunks[0] = generateChunk(0, self.worldBlocks)#generate a random world to the left and right of the center chunk
        gs.generatedChunks[1] = generateChunk(gs.CHUNK_SIZE[0], self.worldBlocks)
        
        self.player = ph.Player((0, 0), gs.blockSize)
        self.camera = cam.Camera(self.player)
        checkChunkUpdates(self.player, self.worldBlocks)
        self.crafter = Crafting(self.screen)
        self.textureNames = ih.fetchTextureNames()
        if(render_mode=="human"):
            self.actionImage=pygame.image.load(self.textureNames["null"]).convert_alpha() #load the image to show block being placed
        self.playerPos = [0, 0]
        self.cursorPos = [0, 0]
        self.isBP=False
       

      
        self.offset = [[-1,-1],[0,-1],[1,-1],  # offsets of player positions, top row is above player
                       [-1,0],[-1,1],[1,0],[1,1],  # left down, left up, right down, right up
                       [-1,2],[0,2],[1,2]]  # below the player
        
        #self.player.rect.y-=6500

    def action(self,action):
        
        fakeKeys = {pygame.K_LEFT: False,pygame.K_RIGHT: False,pygame.K_UP: False,pygame.K_a: False,pygame.K_d: False,
                    pygame.K_w: False,pygame.K_SPACE: False} #list of fake keys the agent can press
        if action in gs.actionSpace["MOVEMENT"]:
            if(self.render_mode=="human"):
                self.actionImage=pygame.image.load(self.textureNames["Movement"]).convert_alpha()
        if action == gs.actionSpace["MOVEMENT"][2]: #jump up
            self.player.jump()
        elif action == gs.actionSpace["MOVEMENT"][1]: #move left
            fakeKeys[pygame.K_LEFT] = True
            self.player.MoveOnX(fakeKeys)
        elif action == gs.actionSpace["MOVEMENT"][3]: #move right
            fakeKeys[pygame.K_RIGHT] = True
            self.player.MoveOnX(fakeKeys)
        elif action == gs.actionSpace["MOVEMENT"][4]: #jump left
            self.player.jump()
            fakeKeys[pygame.K_LEFT] = True
            self.player.MoveOnX(fakeKeys)
        elif action == gs.actionSpace["MOVEMENT"][5]: #jump right
            self.player.jump()
            fakeKeys[pygame.K_RIGHT] = True
            self.player.MoveOnX(fakeKeys)
        elif action in gs.actionSpace["WORLD"]: #if break and place blocks
            self.isBP=True #used to show cursor
            if action in gs.actionSpace["WORLD"][0:10]:
                realAction = action - gs.actionSpace["WORLD"][0] #which block to place
            else:
                realAction = action - gs.actionSpace["WORLD"][10] #which block to break

            self.playerPos = [self.player.getPlayerPos()[0],self.player.getPlayerPos()[1]]
            self.playerPos[0] += self.offset[realAction][0] * gs.blockSize
            self.playerPos[1] += self.offset[realAction][1] * gs.blockSize #add the offset of the block the player wants to break or place to the position of the agent
            self.cursorPos=[self.offset[realAction][0] * gs.blockSize, self.offset[realAction][1] * gs.blockSize] #cursor position is the offset of the block the player wants to break or place
            if action in gs.actionSpace["WORLD"][0:10]:
                if(self.render_mode=="human"):
                    self.actionImage = pygame.image.load(self.textureNames["Block_Break"]).convert_alpha() #load the image to show block being broken
                bph.blockBreak(self.playerPos,self.worldBlocks,self.player,False,False) #break block
            else:
                if(self.render_mode=="human"):
                    self.actionImage = pygame.image.load(self.textureNames["Grass Block"]).convert_alpha() #load the image to show block being placed
                bph.blockPlace(self.playerPos,self.worldBlocks,self.player,False,False) #place block

        elif action in gs.actionSpace["HOTBAR"]:
            if(self.render_mode=="human"):
                self.actionImage = pygame.image.load(self.textureNames["Inv"]).convert_alpha() #load the image to show block being placed
            inv.selectInventory(action - gs.actionSpace["HOTBAR"][0]) #select item anywhere in inventory

        elif action in gs.actionSpace["CRAFTING"]:
            if(self.render_mode=="human"):
                self.actionImage = pygame.image.load(self.textureNames["Crafting Table"]).convert_alpha() #load the image to show currently crafting
            craftingID = action - gs.actionSpace["CRAFTING"][0] #which craftingID to craft
            craftPossibility = self.crafter.craftSpec(craftingID,inv.getInv()) #check if the player can craft the item and performs if possible
        if action not in gs.actionSpace["WORLD"]:
            self.isBP=False #if the agent is not breaking or placing a block, the cursor is not shown
        self.player.update(0,self.worldBlocks)  # may need to change to collison blocks later
        checkChunkUpdates(self.player, self.worldBlocks) #check if the player is in a new chunk and generate a new chunk if needed

    def evaluate(self,prev):
        stages = rw.populateStages()
        current = inv.getInv()
        #print("In stage: ", self.stage)
        
        currStage = stages["Stage" + str(self.stage)]
        rewardInt = currStage.getReward()  # get the reward for the current stage
        completeInt = currStage.getComplete() # get the complete condition for the current stage
        penaltyInt = currStage.getPenalty() # get the penalty for the current stage
        failureInt = currStage.getFailure() # get the failure condition for the current stage
        miscInt = currStage.getMisc() 

        if self.stage == 1:  # collect logs
            # 8 = wooden planks is here because if we get sent back to stage 1
            # we need incentive to break those planks to go back to stage 4 from stage 2
            #stageRewards = {8: 10,7: 10,6: 2,1: 1,0: 3}  # itemID : reward
            stageRewards = {}
            k = 0
            for i in currStage.getGoalItems():
                stageRewards[i] = currStage.getAcquisitionRewards()[k]
                k+=1

            if inv.getItemCountFromInput(7,current) >= 2:  # Complete stage 1
                self.stage += 1
                return completeInt

            for key in stageRewards.keys():
                prevCount = inv.getItemCountFromInput(key,prev)
                currCount = inv.getItemCountFromInput(key,current)

                if prevCount < currCount:  # if broke blocks
                    return stageRewards[key]

                if prevCount > currCount and key == 7:  # If place wood logs
                    return penaltyInt
    
            return miscInt  # any other actions

        elif self.stage == 2:  # craft wooden planks
            # Does not have enough planks and has no logs
            if inv.getItemCountFromInput(7,current) == 0 and inv.getItemCountFromInput(8,current) < 8:
                # has a pickaxe (from stage 4) and has more than 2 wooden planks
                if inv.getItemCountFromInput(8,current) >= 2 and inv.getItemCountFromInput(11,current) > 0:
                    self.stage = 4  # go to stage 4 and try get enough stone
                    return rewardInt-5
                else:  # go back to stage 1
                    self.stage -= 1
                    return failureInt

            # has enough planks to craft a pickaxe -> move to next stage
            elif inv.getItemCountFromInput(8,current) >= 8:
                self.stage += 1
                return completeInt

            planksPrevCount = inv.getItemCountFromInput(8,prev)
            planksCurrCount = inv.getItemCountFromInput(8,current)
            logsPrevCount = inv.getItemCountFromInput(7,prev)
            logsCurrCount = inv.getItemCountFromInput(7,current)

            if logsPrevCount > logsCurrCount:  # less logs than before
                if planksPrevCount < planksCurrCount:
                    return rewardInt+5
                return penaltyInt

            # if sent back to this stage and can break planks that were placed
            if planksPrevCount < planksCurrCount:
                return currStage.getReward()
            
            return miscInt  # any other actions

        elif self.stage == 3:  # craft a wooden pickaxe
            # less than minimum planks to craft one pickaxe and doesn't have a pickaxe
            # go to previous stage
            if inv.getItemCountFromInput(8,current) < 5 and inv.getItemCountFromInput(11,current) == 0:
                self.stage -= 1
                return failureInt

            # has a wooden pickaxe --> move to next stage
            elif inv.getItemCountFromInput(11,current) >= 1:
                self.stage += 1
                return completeInt

            # need 5 wooden planks to make 1 pickaxe
            planksPrevCount = inv.getItemCountFromInput(8,prev)
            planksCurrCount = inv.getItemCountFromInput(8,current)
            pickPrevCount = inv.getItemCountFromInput(11,prev)
            pickCurrCount = inv.getItemCountFromInput(11,current)

            if planksPrevCount > planksCurrCount:  # either placed or crafted using planks
                if pickPrevCount < pickCurrCount:  # crafted a pickaxe
                    return rewardInt
                return penaltyInt  # placed a plank

            return miscInt  # any other action

        elif self.stage == 4:  # collect stone and wooden planks
            #stageRewards = {2: 40,8: 40,7: 10,6: 2,1: 1,0: 3}  # itemID : reward
            stageRewards = {}
            k = 0
            for i in currStage.getGoalItems():
                stageRewards[i] = currStage.getAcquisitionRewards()[k]
                k += 1

            reward = 0
            # might need to reward the agent for selecting the pickaxe
            # if selected == wooden pickaxe
            # return 10 for eg
            # so that the agent can learn to use the pickaxe to break blocks with a higher hardness
            if inv.getSelected().itemID == 11:
                reward += rewardInt
            else:
                reward -= rewardInt

            # has enough resources to move to the next stage
            if inv.getItemCountFromInput(2,current) >= 3 and inv.getItemCountFromInput(8,current) >= 2:
                self.stage += 1
                return completeInt

            # dont have enough planks to craft stone pickaxe
            elif inv.getItemCountFromInput(8,current) < 2:
                self.stage = 2
                return failureInt

            for key in stageRewards.keys():
                prevCount = inv.getItemCountFromInput(key,prev)
                currCount = inv.getItemCountFromInput(key,current)

                if prevCount < currCount:  # break blocks
                    return stageRewards[key] + reward

                if prevCount > currCount:  # place stone or planks
                    if key == 2 or 8:
                        return penaltyInt

            return 0.01 + reward  # other actions

        elif self.stage == 5:  # craft stone pickaxe
            # Have less than minimum stone or wood to craft one pickaxe, and dont have a stone pickaxe
            if inv.getItemCountFromInput(16,current) == 0 and (
                    inv.getItemCountFromInput(2,current) < 3 or inv.getItemCountFromInput(8,current) < 2):
                self.stage -= 1
                return failureInt

            # crafted a stone pickaxe and can move to next stage
            elif inv.getItemCountFromInput(16,current) >= 1:
                self.stage += 1
                return completeInt

            # need 3 stone and 2 planks to craft a stone pickaxe
            stonePrevCount = inv.getItemCountFromInput(2,prev)
            stoneCurrCount = inv.getItemCountFromInput(2,current)
            planksPrevCount = inv.getItemCountFromInput(8,prev)
            planksCurrCount = inv.getItemCountFromInput(8,current)
            pickPrevCount = inv.getItemCountFromInput(16,prev)
            pickCurrCount = inv.getItemCountFromInput(16,current)

            # either placed or crafted using stone or planks
            if stonePrevCount > stoneCurrCount or planksPrevCount > planksCurrCount:
                if pickPrevCount < pickCurrCount:  # crafted pickaxe
                    return rewardInt
                return penaltyInt  # placed stone or planks

            return miscInt # other actions

        elif self.stage == 6:  # collect gold ores, diamond ores and emerald ore
            stageRewards = {}
            k = 0
            for i in currStage.getGoalItems():
                stageRewards[i] = currStage.getAcquisitionRewards()[k]
                k += 1

            reward = 0
            # if we have selected the stone pickaxe
            # otherwise we can't get resources needed
            if inv.getSelected().itemID == 16:
                reward += rewardInt
            else:
                reward -= rewardInt

            # if has enough resouces to move to next stage
            if inv.getItemCountFromInput(46,current) >= 36 and inv.getItemCountFromInput(49,current) >= 36 and inv.getItemCountFromInput(78,current) >= 1:
                self.stage += 1
                return completeInt

            for key in stageRewards.keys():
                prevCount = inv.getItemCountFromInput(key,prev)
                currCount = inv.getItemCountFromInput(key,current)

                if prevCount < currCount:  # break blocks
                    return stageRewards[key] + reward

                if prevCount > currCount:  # placed blocks
                    if key == 46 or 49 or 78:
                        return penaltyInt
            return miscInt + reward  # other actions

        elif self.stage == 7:  # craft diamond, gold ingot and emerald
            enough = inv.getItemCountFromInput(50,current) >= 36 and inv.getItemCountFromInput(47,current) >= 36 and inv.getItemCountFromInput(53,current) >= 1
            # have enough resources to go to the next stage
            if enough:
                self.stage += 1
                return completeInt

            # must've placed the blocks we needed and havent crafted so need to get the blocks again
            elif not enough:
                if inv.getItemCountFromInput(46,current) == 0 and inv.getItemCountFromInput(49,current) == 0 and inv.getItemCountFromInput(78,current) == 0:
                    self.stage -= 1
                    return failureInt
            minerals = [[49,50],[46,47],[78,53]]  # diamond ore, diamond, gold ore, gold, emerald ore, emerald
            for c in minerals:
                OrePrevCount = inv.getItemCountFromInput(c[0],prev)
                OreCurrCount = inv.getItemCountFromInput(c[0],current)
                PrevCount = inv.getItemCountFromInput(c[1],prev)
                CurrCount = inv.getItemCountFromInput(c[1],current)
                if OrePrevCount > OreCurrCount:  # could've placed or crafted  ore
                    if PrevCount < CurrCount:  # crafted a minerals
                        return rewardInt
                    return penaltyInt  # placed the block

            return miscInt  # other actions

        elif self.stage == 8:  # craft diamond, gold blocks
            enough = inv.getItemCountFromInput(64,current) >= 4 and inv.getItemCountFromInput(67,current) >= 4
            # have enough resources to go to the next stage
            if enough:
                self.stage += 1
                return completeInt

            elif not enough:
                if inv.getItemCountFromInput(50,current) < 9 and inv.getItemCountFromInput(47,current) < 9:
                    self.stage -= 1
                    return failureInt

            minerals = [[50,67],[47,64]]  # diamond, diamond block, gold, gold block
            for c in minerals:
                PrevCount = inv.getItemCountFromInput(c[0],prev)
                CurrCount = inv.getItemCountFromInput(c[0],current)
                BlockPrevCount = inv.getItemCountFromInput(c[1],prev)
                BlockCurrCount = inv.getItemCountFromInput(c[1],current)
                if PrevCount > CurrCount:  # could've placed or crafted mineral
                    if BlockPrevCount < BlockCurrCount:  # crafted a mineral
                        return rewardInt
                    return penaltyInt # placed the block (incase mineral becomes placable)

            return miscInt  # random action

        elif self.stage == 9:  # craft the end game block
            # crafted the end game block
            if inv.getItemCountFromInput(83,current) > 0:
                self.done = True
                return completeInt  # game done

            else:  # don't have enough resorces to craft the end game block
                if inv.getItemCountFromInput(67,current) < 4 and inv.getItemCountFromInput(64,current) < 4 and inv.getItemCountFromInput(53,current) == 0:
                    self.stage -= 1
                    return failureInt
            #keep track of the number of blocks we have and compares
            diamondPrevCount = inv.getItemCountFromInput(67,prev)
            diamondCurrCount = inv.getItemCountFromInput(67,current)
            goldPrevCount = inv.getItemCountFromInput(64,prev)
            goldCurrCount = inv.getItemCountFromInput(64,current)
            emeraldPrevCount = inv.getItemCountFromInput(53,prev)
            emeraldCurrCount = inv.getItemCountFromInput(53,current)
            endGamePrevCount = inv.getItemCountFromInput(83,prev)
            endGameCurrCount = inv.getItemCountFromInput(83,current)

            if diamondPrevCount > diamondCurrCount or goldPrevCount > goldCurrCount or emeraldPrevCount > emeraldCurrCount:
                if endGamePrevCount < endGameCurrCount:  # crafted end game block
                    return completeInt
                return failureInt  # placed blocks

            return miscInt  # other actions

    def getPrevInv(self): # used for inventory comparison
        return copy.deepcopy(inv.getInv())        
   

    def is_done(self): # check game state based on reward system
        if self.done:
            return True  # game done
        else:
            return False

    def observe(self):
        # returns the current state of the game in RGBA format
        img = pygame.image.tostring(self.screen, "RGBA")
        newScreen = pygame.image.fromstring(img, (gs.width, gs.height), "RGBA")
        rgbarr = np.array(pygame.surfarray.pixels3d(newScreen), dtype=np.float32)
        return rgbarr

   
    def view(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit()

        # DO drawing
        bg = pygame.image.load(self.textureNames["Sky"]).convert()
        bg = pygame.transform.scale(bg, (gs.width, gs.height))
     
        self. screen.blit(bg, (0, 0))
       # bg = pygame.Rect(0,0,gs.width,gs.height) #no background image to save resources
       # pygame.draw.rect(self.screen,(0,0,0),bg)
        self.collisionblocks = self.camera.draw(self.screen,self.worldBlocks)
        inv.drawHotBar(self.screen)  # --> draw inventory
        relative=gs.blockSize/30
        font = pygame.font.Font('MainGame/Font/Minecraft.ttf',int(16 * relative))
        text = font.render("ACTION", 1*relative, (255, 255,255))
        if(self.render_mode=="human"):
            pygame.draw.rect(self.screen,(90,90,90),[900*relative,20*relative,85*relative,100*relative],0)
            self.screen.blit(text, (910*relative, 30*relative))
            self.actionImage=pygame.transform.scale(self.actionImage, (55*relative,55*relative))
            self.screen.blit(self.actionImage, (915*relative, 50*relative))
        blockFrameImg = pygame.image.load(self.textureNames["Block_Frame"]).convert_alpha() # --> load block cursor texture
        blockFrame = pygame.transform.scale(blockFrameImg, (gs.blockSize, gs.blockSize)) # --> scale block cursor texture
        #blockPos = gs.getPos(mousePos)[0] - camera.getOffsets()[0] % gs.blockSize, \ gs.getPos(mousePos)[1] - camera.getOffsets()[1] % gs.blockSize
        if(self.isBP): #if block placing
            self.cursorPos[0] +=  self.camera.hWidth  # --> add camera offset
            self.cursorPos[1] +=  self.camera.hHeight # --> add camera offset
            #further offset to center the block, aka lock to grid
            blockPos =gs.getPos( (self.cursorPos))[0] - self.camera.getOffsets()[0] % gs.blockSize, gs.getPos( (self.cursorPos))[1] - self.camera.getOffsets()[1] % gs.blockSize
            self.screen.blit(blockFrame,blockPos)  #blits the block frame at the block position
            
        if (self.render_mode == "human"):
            pygame.display.flip()
        # else:
        # pygame.display.update()
        self.clock.tick(self.game_speed)
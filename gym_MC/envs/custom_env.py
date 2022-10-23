import gym
from gym import spaces
import numpy as np
from gym_MC.envs.minecraftEnv import MinePy
import gameSettings as gs
import inventoryHandler

class CustomEnv(gym.Env):
    #if render mode is human, render game to screen- if it is None- render game to surface
    metadata = {"render_modes" : ["human","rgb_array"],"render_fps": 60,"easyStart":[0,1,2]}
    def __init__(self,render_mode="human",easyStart=0,seed=None):
        self.seed=seed
        if(self.seed == None):
            self.seed = gs.genRandomSeed()
        gs.seed=self.seed
        self.pygame = MinePy(render_mode,easyStart,seed=gs.seed)
        self.action_space = spaces.Discrete(75)
        self.observation_space = spaces.Box(np.array([0, 0], dtype=np.float32), np.array([10, 10], dtype=np.float32)) #low=0 high =255 shape is (width,height,3)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.easyStart = easyStart
        

    def reset(self, seed=None, options=None): #seems to be called all way too frequently
        super().reset(seed=seed, options=options)
        self.seed=seed
        #gs.seed=self.seed
        if(self.seed == None):
            self.seed = gs.genRandomSeed()
        gs.seed=self.seed
        del self.pygame
        self.pygame = MinePy(self.render_mode,self.easyStart,seed=gs.seed)
        obs = self.pygame.observe()
        infoDict = {
            "inventory" : inventoryHandler.getInv()
        }
        return (obs, infoDict)

    def render(self):
        if(self.render_mode=="human"):
            self.pygame.view()

    def step(self, action):
        prevInv = self.pygame.getPrevInv()
        obs = self.pygame.observe()
        self.pygame.action(action)
        done = self.pygame.is_done()
        infoDict = {
                "inventory" : inventoryHandler.getInv()
            }
        reward = self.pygame.evaluate(prevInv)
        self.render()
        return obs, reward, done, False, infoDict
    
    
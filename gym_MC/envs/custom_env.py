import gym
from gym import spaces
import numpy as np
from gym_MC.envs.minecraftEnv import MinePy
import gameSettings as gs
import inventoryHandler
class CustomEnv(gym.Env):
    #if render mode is human, render game to screen- if it is None- render game to surface
    metadata = {"render_modes" : ["human"],"render_fps": 64}
    def __init__(self,render_mode="human"):
        self.pygame = MinePy()
        self.action_space = spaces.Discrete(75)
        self.observation_space = spaces.Box(np.array([0, 0], dtype=np.float32), np.array([10, 10], dtype=np.float32)) #low=0 high =255 shape is (width,height,3)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def reset(self, seed=None, options=None): #seems to be called all way too frequently
        super().reset(seed=seed, options=options)
        gs.seed = seed
        del self.pygame
        self.pygame = MinePy()
        obs = self.pygame.observe()
        
        infoDict = {
            "inventory" : inventoryHandler.getInv()
        }
        return (obs, infoDict)

    def step(self, action):
        obs = self.pygame.observe()
        prevInv = inventoryHandler.getInv()
        self.pygame.action(action)
        done = self.pygame.is_done()
        infoDict = {
                "inventory" : inventoryHandler.getInv()
            }
        reward = self.pygame.evaluate(prevInv)
        return obs, reward, done, False, infoDict

    def render(self):
        if(self.render_mode=="human"):
            self.pygame.view()
    
    
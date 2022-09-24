import gym
from gym import spaces
import numpy as np
from gym_MC.envs.minecraftEnv import MinePy

class CustomEnv(gym.Env):
    #if render mode is human, render game to screen- if it is None- render game to surface
    metadata = {"render_modes" : ["human"],"render_fps": 64}
    def __init__(self,render_mode="human"):
        self.pygame = MinePy()
        self.action_space = spaces.Discrete(75)
        self.observation_space = spaces.Box(np.array([0, 0]), np.array([10, 10])) #low=0 high =255 shape is (width,height,3)
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def reset(self): #seems to be called all way too frequently
        del self.pygame
        self.pygame = MinePy()
        obs = np.array(self.pygame.observe())
        return obs

    def step(self, action):
        prevObs = self.pygame.observe()
        self.pygame.action(action)
        reward = self.pygame.evaluate(prevObs)
        done = self.pygame.is_done()
        return prevObs, reward, done, {},{}

    def render(self):
        if(self.render_mode=="human"):
            self.pygame.view()
    
    
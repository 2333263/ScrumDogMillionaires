import gym
from gym import spaces
import numpy as np
from gym_MC.envs.minecraftEnv import MinePy

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = MinePy()
        self.action_space = spaces.Discrete(75)
        self.observation_space = spaces.Box(np.array([0, 0]), np.array([10, 10])) #low=0 high =255 shape is (width,height,3)

    def reset(self):
        del self.pygame
        self.pygame = MinePy()
        obs = np.array(self.pygame.observe(),dtype=np.float32)
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {},{}

    def render(self, mode="human", close=False):
        self.pygame.view()
        
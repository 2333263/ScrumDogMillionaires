import gym
from gym import spaces
import numpy as np
from gym_MC.envs.minecraftEnv import MinePy

class CustomEnv(gym.Env):
    #metadata = {'render.modes' : ['human']}
    def __init__(self):
        self.pygame = MinePy()
        self.action_space = spaces.Discrete(72)
        self.observation_space = spaces.Box(np.array([0, 0]), np.array([10, 10])) ##im not sure how to change this

    def reset(self):
        del self.pygame
        self.pygame = MinePy()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done = self.pygame.is_done()
        return obs, reward, done, {}

    def render(self, mode="human", close=False):
        self.pygame.view()
        
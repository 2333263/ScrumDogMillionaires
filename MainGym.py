import random 
import gym 
import gym_MC
import gameSettings as gs

env = gym.make("MinePy-1")
env.reset()
for episode in range(100000):
    action = random.choice([i for i in range(0, 72, 1)])
    env.step(action)
    env.render()
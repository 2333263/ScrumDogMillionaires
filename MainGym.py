import random 
import gym 
import gym_MC
import gameSettings as gs

env = gym.make("MinePy-1")
env.reset()
for episode in range(100000):
    action = random.choice(gs.actionSpace["WORLD"])
    env.step(action)
    env.render()
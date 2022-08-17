import random 
import gym 
import gym_MC

env = gym.make("MinePy-1")
env.reset()
for episode in range(100000):
    action = random.choice([0, 1, 2])
    env.step(action)
    #env.render()
import random 
import gym
import gym_MC

#Create the gym environment 
env = gym.make("MinePy-1", render_mode="human", easyStart=0, seed=1212)
#env.action_space.seed(45)

#Gets the osbervations and info before reset 
obs, info = env.reset(seed=1212)
done=False

#Loops random actions for the agent obvervations 
for episode in range(10000):
    action = random.choice([i for i in range(0, 75, 1)])
    
    #Advance the agent to the next step
    env.step(action)
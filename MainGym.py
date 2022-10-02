import random 
import gym 
import gym_MC
import gameSettings as gs

from gym.version import VERSION
print("GYM VERSION: ", VERSION)

env = gym.make("MinePy-1", render_mode="human")
env.action_space.seed(gs.seed)
obs = env.reset(seed=gs.seed)
done=False
for episode in range(100000):
    action = random.choice([i for i in range(0, 75, 1)])
    #action=gs.actionSpace["MOVEMENT"][4]
    #if (done==False):
     #   for i in range(10):
      #      env.step(-1)
       #     env.render()
        #    done=True
    env.step(action)
    env.render()
    
    #make sure crafting only happens in range of crafting table
    #generate a crafting table in the chunks
    #
## Setting up the Agent

<!-- Environment variables,  -->

Ensure you have the following code in your file:

```py
import gym
import gym_MC

env = gym.make("MinePy-1", render_mode="human",easyStart=0,seed=1024, spawnLoc=(1024,1024), task="1")

obs, info = env.reset(seed=1212) #has to be the same seed as above
done=False

```

## Setting up new environments
render_mode:  

* `human`: renders the game to a screen. 
* `rgb_array`: returns the screen as a 2d array of pixel colour values.

  

easyStart:  

* `0:` no extra items.

* `1:` player starts with wooden pickaxe and 4 wooden planks.

* `2:` player starts with wooden pickaxe and 4 wooden planks, a stone pickaxe, a diamond and an emerald.

  

seed:

* integer value that acts as seed for both the world and the AI.

  
spawnLoc:

* Takes in a pair of ints, and sets the agents spawn location.
* If none is given, default spawn location is (0,0).
* Note that on a reset, if no spawn location is given, but one was given in the original initilization, the spawn location will be the one given in the intilization.
* Also note that the position is in blocks not pixels.

task:

* Number between 1 and 9 that sets the goal of the agent

    - `1`: The agent must collect 2 or more wooden logs.

    - `2`: All the requirements of stage 1 and the agent mut craft 8 or more wooden planks.

    - `3`: All the requirements of stage 2 and the agent must craft 1 or more wooden pickaxes.

    - `4`: All the requirements of stage 3 and the agent must collect 3 stone, as well as have 2 wooden planks in its inventory.

    - `5`: All the requirements of stage 4 and the agent must craft a stone pickaxe.

    - `6`: All the requirements of stage 5 and the agent must collect 36 gold ore, 36 diamond ore and 1 emerald ore.

    - `7`: All the requirements of stage 6 and the agent must craft 9 diamonds, 9 gold ingots and 1 emerald.

    - `8`: All the requirements of stage 7 and the agent must craft 4 diamond blocks and 4 gold blocks.

    - `9`: All the requirements of stage 8 and the agent must craft the end game block.
* 

In order to perform an action use the following:

```py

env.step(step)

```

where step is an integer value between 0 and 75, representing an action the player can take.

* `0:` no action.

* `1-4:` movement actions.

* `4-24:` break and placing actions.

* `25-64:` change selected item.

* `65-74:` when next to a crafting table, it will craft a specific item.

## Other functions

* `reset:` takes same options as above and resets the game.

* `render:` forces game to render.

* `step:` takes in an action, steps the agent forward, returns observations, reward, whether or not the game is done, and an dictionary of information, and will render if render mode is set to human.


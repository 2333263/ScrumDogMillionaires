## Setting up the Agent

<!-- Environment variables,  -->

Ensure you have the following code in your file:

```python3
import gym
import gym_MC

env = gym.make("MinePy-1", render_mode="human",easyStart=0,seed=)

```

## Setting up new environments
render_mode:  

* `human`: renders the game to a screen  
* `rgb_array`: returns the screen as a 2d array of pixel colour values

  

easyStart:  

* `0:` no extra items

* `1:` player starts with wooden pickaxe and 4 wooden planks

* `2:` player starts with wooden pickaxe and 4 wooden planks, a stone pickaxe, a diamond and an emerald

  

seed:

* integer value that acts as seed for both the world and the AI

  

In order to perform an action use the following:

```python3

env.step(step)

```

where step is an integer value between 0 and 75, representing an action the player can take.

* `0:` no action

* `1-4:` movement actions

* `4-24:` break and placing actions

* `25-64:` change selected item

* `65-74:` when next to a crafting table, it will craft a specific item

## Other functions

* `reset:` takes same options as above and resets the game

* `render:` forces game to render

## Creating new rewards

  

## Using built in tasks for the agent

  

## Adding new tasks for the agent

  


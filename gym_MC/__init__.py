from gym.envs.registration import register
#from .envs import CustomEnv
register(
    id='MinePy-1',
    entry_point='gym_MC.envs:CustomEnv',
    max_episode_steps=2000,
    new_step_api = True
)
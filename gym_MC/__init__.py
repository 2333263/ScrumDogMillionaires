from gym.envs.registration import register

register(
    id='MinePy-1',
    entry_point='gym_MC.envs:CustomEnv',
    max_episode_steps=2000
)
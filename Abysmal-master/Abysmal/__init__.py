from gym.envs.registration import register

register(
    id='Abysmal-v0',
    entry_point='Abysmal.envs:AbysmalEnv',
    timestep_limit=1000,
)

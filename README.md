# Abysmal

#example
```python
import gym
import Abysmal
import time
import copy


env = gym.make('Abysmal-v0')
env.reset()

for _ in range(500):
    action = env.action_space.sample()
    if(_==10):env.render()
    observation, reward, done, info = env.step(0)
    info['aa']=1
    print("reward= ",reward)
    if(done==1):
        env.reset()


```
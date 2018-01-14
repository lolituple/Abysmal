import os
import numpy as np
import gym
import random
import sys
import cv2
from gym import spaces
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk
from PIL import Image, ImageTk

RE_OVERFLOW=2
Num_num=1

dir_str=os.path.dirname(os.path.realpath(__file__))+'/mnist.npz'
f = np.load(dir_str)
x_train = f['x_train']
y_train = f['y_train']
f.close()
Num=np.zeros((10,Num_num,28,28))
for i in range(10):
    id=np.array(np.where(y_train==i))
    id=np.reshape(id,-1)
    id=np.random.permutation(id)
    id=id[0:Num_num]
    Num[i,:]=x_train[id]
        
class AbysmalEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    viewer=None
    def __init__(self):
        self.num1=self.Ran()
        self.num2=0
        self.GetPic()
        
        self.pro_id=0
        self.iter_num=0
        self.avg_reward=0
        self.avg_gamelen=0
        
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(0, 256, [28,28,1])
        #self.observation_space = spaces.Box(0, 256, [20])
        super(AbysmalEnv, self).__init__()
    
    def _seed(self,A):
        self.pro_id=A[0]
        self.iter_num=A[1]
        self.avg_reward=A[2]
        self.avg_gamelen=A[3]
        
    def GetPic(self):
        self.num1_pic=random.randint(0,Num_num-1)
        self.num2_pic=random.randint(0,Num_num-1)
    def Ran(self):
        #return random.randint(1,9)
        '''
        for i in range(9):
            o=random.randint(0,1)
            if(o==0):
                return i+1
        return 9
        '''
        return random.randint(9,9)
    
    def _render(self, mode='human', close=False):
        '''
        state=np.zeros((28,56))
        state[:,0:28]=Num[self.num1][self.num1_pic]
        state[:,28:56]=Num[self.num2][self.num2_pic]
        cv2.imshow("Image", state)
        cv2.destroyAllWindows()
        '''
        print('Num1=',self.num1,'Num2=',self.num2)

    def _reset(self):
        self.__init__()
        return self.CreateState()
    #def _close(self):

    def CreateState(self):
        state=np.zeros((28,28,1))
        state[:,:,0]=Num[self.num2][self.num2_pic]
        #state[:,:,1]=Num[self.num1][self.num1_pic]
        return state
        '''
        state=np.zeros((20))
        state[self.num1+0]=1
        state[self.num2+10]=1
        return state
        '''
        
    def _step(self,actions):
        done=0
        reward=0
        
        BAD_END=max(1-(self.iter_num/200.0),0)
        HAPPY_END=max(0-(self.iter_num/200.0),0)
        
        if(actions==0):
            if(self.num1+self.num2>9):
                done=1
                reward=BAD_END*self.num2-RE_OVERFLOW
            else:
                self.num2+=self.num1
                #reward-=RE_ROUND
                self.num1=self.Ran()
        if(actions==1):
            reward=self.num2+HAPPY_END
            done=1
        self.GetPic()
        return (self.CreateState(),reward,done,{})
        

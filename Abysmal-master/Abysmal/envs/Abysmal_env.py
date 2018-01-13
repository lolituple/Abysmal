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

RE_WAIT=0.5
RE_OVERFLOW=2
RE_ROUND=0.1
Num_num=50

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
class Viewer(tk.Tk):

    def __init__(self, evn):
        self.evn=evn
        super(Viewer, self).__init__()
        self.origin = np.array([20, 20])

        dir_str=os.path.dirname(os.path.realpath(__file__))+'/'
        self.walls_image=ImageTk.PhotoImage(Image.open(dir_str+'walls.png'))
        self.boxes_image=ImageTk.PhotoImage(Image.open(dir_str+'boxes.png'))
        self.item_fig={}
        self.item_fig['*']=ImageTk.PhotoImage(resize(Image.open(dir_str+'item1.png')))
        self.item_fig['^']=ImageTk.PhotoImage(resize(Image.open(dir_str+'item2.png')))
        self.bomb_pic=ImageTk.PhotoImage(resize(Image.open(dir_str+'bomb.png')))
        self.player0_pic=ImageTk.PhotoImage(resize(Image.open(dir_str+'player0.png')))
        self.player1_pic=ImageTk.PhotoImage(resize(Image.open(dir_str+'player1.png')))

        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)

        self.init_image()
        
    def Text(self,xy,v):
        t=self.canvas.create_text(xy[0]*UNIT+20,xy[1]*UNIT+8,anchor='center',text=str(v))
        return t
    def render(self):
        self.reset()
        self.title('Crazy Arcade')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        
        
        self.update()
    
    def init_image(self):
        self.maze=self.evn.maze
        self.players=self.evn.players
        self.players[0].fig=self.player0_pic
        self.players[1].fig=self.player1_pic
        self.inpulse=self.evn.inpulse
        self.boxes_xyk=self.evn.boxes_xyk
        #self.bombs_data
        #self.bombs_xy

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        
        # create origin
        origin = self.origin
        
        #create wall,box,item,bombs
        boxes_xy=[]
        for box in self.boxes_xyk:
            boxes_xy.append((box[0],box[1]))
        for x in range(0,MAZE_W):
            for y in range(0,MAZE_H):
                if (self.maze[x][y]=='#'):
                    wall_now = origin*2 + np.array([UNIT*x+2, UNIT*y+2])
                    self.walls = self.canvas.create_image(wall_now[0],
                        wall_now[1], anchor='se',
                        image=self.walls_image)
                position = self.origin*2 + np.array([UNIT*x+2, UNIT*y+2])
                if (x,y) in boxes_xy:
                    self.canvas.create_image(position[0],
                        position[1], anchor='se',
                        image=self.boxes_image)
                else:
                    if(self.maze[x][y] in ['*','^']):
                        self.canvas.create_image(position[0],
                            position[1], anchor='se',
                            image=self.item_fig[self.maze[x][y]])
                if (x,y) in self.evn.bombs_xy:
                    self.canvas.create_image(origin[0]+x*UNIT,origin[1]+y*UNIT, anchor='center', image=self.bomb_pic)
        
        # create players
        for player_id in range(2):
            xy_now=self.players[player_id].xy
            player_now = origin + np.array([UNIT*xy_now[0], UNIT*xy_now[1]])
            self.players[player_id].players = self.canvas.create_image(player_now[0], \
                player_now[1], anchor='center', \
                image=self.players[player_id].fig)
            
        #create inpulse
        for i in range(MAZE_W):
            for j in range(MAZE_H):
                if(self.inpulse[i][j]==1):
                    position = self.origin + np.array([UNIT*i, UNIT*j])
                    
                    self.inpulse.append(self.canvas.create_rectangle(
                    position[0] - 10, position[1] - 10,
                    position[0] + 10, position[1] + 10,
                    fill="#FF4444"))

        # create text for bombs
        for i in range(self.evn.bombs_cnt):
            self.Text(self.evn.bombs_xy[i],self.evn.bombs_data[i][0])
        
        # pack all
        self.canvas.pack()
        
    def reset(self):
        self.canvas.delete("all")
        self.init_image()
    
        
class AbysmalEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    viewer=None
    def __init__(self):
        self.num1=self.Ran()
        self.num2=0
        self.GetPic()
        
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(0, 256, [28,28,2])
        #self.observation_space = spaces.Box(0, 256, [20])
        super(AbysmalEnv, self).__init__()
    
    #def _seed(self,A):

    def GetPic(self):
        self.num1_pic=random.randint(0,Num_num-1)
        self.num2_pic=random.randint(0,Num_num-1)
    def Ran(self):
        #return random.randint(1,9)
        return 1   
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
        state=np.zeros((28,28,2))
        state[:,:,0]=Num[self.num1][self.num1_pic]
        state[:,:,1]=Num[self.num2][self.num2_pic]
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
        
        if(actions==0):
            if(self.num1+self.num2>9):
                done=1
                reward-=RE_OVERFLOW
                reward+=self.num2
            else:
                self.num2+=self.num1
                reward-=RE_ROUND
                self.num1=self.Ran()
                
        if(actions==1):
            reward-=RE_WAIT
            self.num1=self.Ran()
        if(actions==2):
            reward=self.num2
            done=1
        self.GetPic()
        return (self.CreateState(),reward,done,{})
        

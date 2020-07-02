
import gym
from gym import spaces
import numpy as np
import random


# 自定义环境
class Myenv(gym.Env):
    def __init__(self):

        # [a0, a1, a2, a3]  # 可分别取值 1/2/3   4/5   4/5   4/5
        #self.action_space = spaces.Box(np.array([1, 4, 4, 4]), np.array([3, 5, 5, 5]), dtype=np.int)
        self.action = 0
        self.action_list = [[i,j,l,k] for i in range(1,4) for j in range(4,6) for l in range(4,6) for k in range(4,6)]

        # [n0, n1, n2, n3, n4, n5]  A-1-2-3-4-5  共6个状态
        #self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0]), np.array([10, 2, 4, 8, 6, 5]), dtype=np.int)
        self.observation = np.zeros((1,6))  # A 1 2 3 4 5

        self.a_send = random.randint(1,100)
        self.start = [self.a_send, 0, 0, 0, 0, 0]    # 初始A的发送数据量
        self.state = self.start             # 初始state

        self.count = 0  # 用来计数，过了几秒
        self.total_A = 0
        self.total_B = 0

        # 节点A, 1、2、3、4、5的发送数据能力
        self.max_ability = [self.state[0], 20, 40, 60, 30, 10]

#     def action_list(self):
#         action_list = []
#         for i in range(1,4):
#             for j in range(4,6):
#                 for k in range(4,6):
#                     for l in range(4,6):
#                         action_list.apend([i,j,k,l])



    def step(self, action):

        action = self.action_list[action]
        print("\n")
        print("No." + str(self.count+1) + "s:")
        self.a_send = random.randint(1, 100)
        self.state[0] = self.a_send

        print("A_sends = " + str(self.state[0]))
        print("state_0 = " + str(self.state))
        print("action = " + "[A->" + str(action[0]) + ", " + "1->" + str(action[1]) + ", " + "2->" + str(action[2])
              + ", " + "3->" + str(action[3]) + "]")


        forward = []
        forward.append(self.a_send)   # A要发送的数据

        for i in range(1, len(self.max_ability)):
            forward.append(min(self.state[i], self.max_ability[i]))


        print("forward = " + str(forward))

        # 各个state减去发送出去的数据
        for i in range(1, len(self.state)):  # 更新1 2 3的state

            self.state[i] = self.state[i] - forward[i] # 1 2 3 4 5发送出去了

        print("state_sub = " + str(self.state))

        # 各个state加上传来的数据
        for i in range(len(action)):
            send_to_state = action[i]  # 发送给的state

            if i == 0:  # 从A发送
                self.state[send_to_state] += forward[0]

            else:  # 从 i = 1/2/3 发送给 4/5
                self.state[send_to_state] += forward[i]



        print("state_plus = " + str(self.state))

        self.count += 1
        self.total_A += self.a_send
        self.total_B += (forward[4] + forward[5])

        print("A_send = " + str(self.a_send))
        print("B_receive = " + str(forward[4] + forward[5]))

        if self.count == 5:
            print("total_A_in_5s = " + str(self.total_A))
            print("total_B_in_5s = " + str(self.total_B))
            reward = self.total_B / (self.total_A + 1)
            
        else:
            reward = 0
        
        done = False


        return self.state, reward, done

    # 用于在每轮开始之前重置智能体的状态，把环境恢复到最开始
    def reset(self):
        self.a_send = random.randint(1, 100)
        self.start = [self.a_send, 0, 0, 0, 0, 0]  # 初始A的发送数据量
        self.state = self.start  # 初始state

        self.count = 0  # 用来计数，过了几秒
        self.total_A = 0
        self.total_B = 0

        self.count = 0
        return self.state

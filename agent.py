import random
import torch
import random
import numpy as np

from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        # self.table = [[[10 for _ in range(2)] for _ in range(5)] for _ in range(6)]
        # self.alpha = 0.01
        # self.gamma = 0.90
        # self.epsilon = 10
        # table[x][y][z] refers to state action value : tasksize=x, timeout=y, action=z see get_state in edgeDevice once, using optimistic initial values
        self.time_step = 0
        self.epsilon = 5  # randomness
        self.gamma = 0.99  # discount rate
        # self.memory = deque(maxlen=MAX_MEM) #popleft()
        self.model = Linear_QNet(2, 256, 2)  # input,hidden,output
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, state):
        return state

    # def remember(self, state, action, reward, next_state, done):
    #     self.memory.append(
    #         (state, action, reward, next_state, done)
    #     )  # popleft if MAX_MEM is reached

    # def train_long_memory(self):
    #     if len(self.memory) > BATCH_SIZE:
    #         mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
    #     else:
    #         mini_sample = self.memory
    #     states, actions, rewards, next_states, dones = zip(*mini_sample)
    #     self.trainer.train_step(states, actions, rewards, next_states, dones)

    def update(self, state, action, reward, next_state):
        # self.table[state[0]][state[1]][action] = self.table[state[0]][state[1]][
        #     action
        # ] + self.alpha * (
        #     reward
        #     + self.gamma * max(self.table[next_state[0]][next_state[1]])
        #     - self.table[state[0]][state[1]][action]
        # )
        self.trainer.train_step(state, action, reward, next_state)

    def get_action(self, state, t):
        # tradeoff exploration/exploitation
        final_move = 0
        # return 0

        if random.randint(0, 100) < self.epsilon:
            final_move = random.randint(0, 1)

        else:
            # final_move = max(
            #     enumerate(self.table[state[0]][state[1]]), key=lambda x: x[1]
            # )[0]
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()
            print("Action : ", final_move)
        return final_move

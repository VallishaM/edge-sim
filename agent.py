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
        self.time_step = 0
        self.epsilon = 10  # randomness
        self.gamma = 0.90  # discount rate
        # self.memory = deque(maxlen=MAX_MEM) #popleft()
        self.model = Linear_QNet(4, 256, 2)  # input,hidden,output
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, state):
        return np.array(state, dtype=int)

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
        self.trainer.train_step(state, action, reward, next_state)

    def get_action(self, state):
        # tradeoff exploration/exploitation
        final_move = 0
        if random.randint(0, 100) < self.epsilon:
            move = random.randint(0, 1)
            final_move = 1
        else:

            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move = move
        return final_move

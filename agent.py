import random
import torch
import random
import numpy as np
from collections import deque
from model import DeepQNetwork, QTrainer
from helper import plot

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.01

class Agent:
    def __init__(self):
        self.epsilon = 10  # randomness
        self.gamma = 0.99  # discount rate
        self.memory = deque(maxlen=MAX_MEM) #popleft()
        self.model = DeepQNetwork(5, 2)  # input,output
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))  # popleft if MAX_MEM is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, True)

    def train_short_memory(self, state, action, reward, next_state):
        self.trainer.train_step(state, action, reward, next_state)

    def update(self, state, action, reward, next_state):
        self.train_short_memory(state, action, reward, next_state)
        self.remember(state, action, reward, next_state)

    def get_action(self, state, t):
        final_move = 0
        # Exploration / Exploitation tradeoff
        if random.randint(0, 100) < self.epsilon:
            final_move = random.randint(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()
            print("Action : ", final_move)

        return final_move
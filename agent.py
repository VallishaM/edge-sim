import random
import torch
import numpy as np
from model import DeepQNetwork
from helper import plot
import os
import torch.nn.functional as F

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.01

class Agent:
    def __init__(self,type):
        self.alpha = 0.01
        self.gamma = 0.99
        self.epsilon = 10
        self.memory = list()
        self.type = type
        self.tau = 0.001
        if os.path.exists('./model/model-DMORL.pt'):
            self.model =  torch.load('./model/model-DMORL.pt')
            self.target_model = torch.load('./model/target_model-DMORL.pt')
            self.model.eval()
        else:
            self.model = DeepQNetwork(5, 2)  # input,output
            self.target_model = DeepQNetwork(5, 2)
            for target_param, param in zip(self.model.parameters(), self.target_model.parameters()):
                target_param.data.copy_(param)

        self.optimizer1 = torch.optim.Adam(self.model.parameters())
        self.optimizer2 = torch.optim.Adam(self.target_model.parameters())

    def remember(self, state, action, reward, next_state):
        if len(self.memory) == MAX_MEM:
            self.memory.pop(0)
        self.memory.append((state, action, reward, next_state))  # popleft if MAX_MEM is reached

    def update(self, state, action, reward, next_state):
        self.remember(state, action, reward, next_state)

        if len(self.memory) > BATCH_SIZE:
            batch = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            batch = self.memory
        loss1, loss2 = self.compute_loss(batch)

        self.optimizer1.zero_grad()
        loss1.backward()
        self.optimizer1.step()

        self.optimizer2.zero_grad()
        loss2.backward()
        self.optimizer2.step()

    def get_action(self, state, t):
        final_move = 0
        # Exploration / Exploitation tradeoff
        if random.randint(0, 100) < self.epsilon:
            final_move = random.randint(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()

        return final_move
    
    def save(self):
        self.model.save(file_name="model-DMORL.pt")
        self.target_model.save(file_name="target_model-DMORL.pt")

    
    def compute_loss(self, batch):     
        states, actions, rewards, next_states = [], [], [], []
        for i in range(len(batch)):
            states.append(batch[i][0])
            actions.append(batch[i][1])
            rewards.append(batch[i][2])
            next_states.append(batch[i][3])
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)
        rewards = rewards.view(rewards.size(0), 1)

        # resize tensors
        actions = actions.view(actions.size(0))

        # compute loss
        curr_Q1, i = torch.max(self.model.forward(states), 1)
        curr_Q2, i = torch.max(self.target_model.forward(states), 1)
        curr_Q1 = curr_Q1.view(curr_Q1.size(0), 1)
        curr_Q2 = curr_Q2.view(curr_Q2.size(0), 1)

        next_Q1 = self.model.forward(next_states)
        next_Q2 = self.target_model.forward(next_states)
        next_Q = torch.min(
            torch.max(self.model.forward(next_states), 1)[0],
            torch.max(self.target_model.forward(next_states), 1)[0]
        )
        next_Q = next_Q.view(next_Q.size(0), 1)
        expected_Q = rewards + self.gamma * next_Q

        loss1 = F.mse_loss(curr_Q1, expected_Q.detach())
        loss2 = F.mse_loss(curr_Q2, expected_Q.detach())

        return loss1, loss2
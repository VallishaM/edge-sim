import random
import torch
import numpy as np
from model import DeepQNetwork
from helper import plot
import os
import torch.nn.functional as F

MAX_MEM = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self,type):
        self.alpha = 0.01
        self.gamma = 0.99
        self.epsilon = 10
        self.memory = list()
        self.type = type
        self.tau = 0.01
        self.criterion = torch.nn.MSELoss()
        
        if os.path.exists('./model/actor.pt'):
            self.actor =  torch.load('./model/actor.pt')
            self.actor_target = torch.load('./model/actor-target.pt')
            self.actor.eval()
            self.actor_target.eval()

            self.critic =  torch.load('./model/critic.pt')
            self.critic_target = torch.load('./model/critic-target.pt')
            self.critic.eval()
            self.critic_target.eval()
        else:
            self.actor = DeepQNetwork(5, 2)  # input,output
            self.actor_target = DeepQNetwork(5, 2)
            for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
                target_param.data.copy_(param.data)

            self.critic = DeepQNetwork(7, 2)  # input,output
            self.critic_target = DeepQNetwork(7, 2)
            for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
                target_param.data.copy_(param.data)

        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), lr=3e-2)
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), lr=1e-2)

        self.actor_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.actor_optimizer, 'min')
        self.critic_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(self.critic_optimizer, 'min')

    def remember(self, state, action, reward, next_state):
        if len(self.memory) == MAX_MEM:
            self.memory.pop(0)
        self.memory.append((state, action, reward, next_state))  # popleft if MAX_MEM is reached

    def update(self, state, action, reward, next_state, time_step):
        self.remember(state, action, reward, next_state)

        if time_step % 25 == 0 and time_step > 0:
            if len(self.memory) > BATCH_SIZE:
                batch = random.sample(self.memory, BATCH_SIZE)  # list of tuples
            else:
                batch = self.memory
        else:
            batch = [[state, [action], [reward], next_state]]

        states, actions, rewards, next_states = [], [], [], []
        for i in range(len(batch)):
            states.append(batch[i][0])
            actions.append([batch[i][1]])
            rewards.append(batch[i][2])
            next_states.append(batch[i][3])
        states = torch.FloatTensor(states)
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(next_states)

        # resize tensors
        actions = actions.view(actions.size(0))
        rewards = rewards.view(rewards.size(0))

        # critic loss
        Qvals, i = torch.max(self.critic_target.forward(self.cat(self.cat(states, actions), rewards)), 1)
        # print("Qvals: ", Qvals)

        exp_rewards, i = torch.max(self.actor_target.forward(next_states), 1)
        next_actions = torch.argmax(self.actor_target.forward(next_states), 1)
        # print("next_actions: ", next_actions)

        l = self.cat(self.cat(next_states, next_actions), exp_rewards)
        # print("l: ", l)

        next_Q, i = torch.max(self.critic_target.forward(l), 1)
        # print("next_Q: ", next_Q)

        Qprime = torch.add(rewards, torch.Tensor([ self.gamma * q for q in next_Q ]))
        # print("Qprime: ", Qprime)
        critic_loss = self.criterion(Qvals, Qprime)

        # actor loss
        Qvals, i = torch.max(self.actor.forward(states), 1)
        exp_rewards, i = torch.max(self.actor.forward(states), 1)
        actions = torch.argmax(self.actor.forward(states), 1)

        l = self.cat(self.cat(states, actions), exp_rewards)
        policy_loss = -self.critic.forward(l)
        policy_loss = policy_loss.mean()

        self.actor_optimizer.zero_grad()
        policy_loss.backward()
        self.actor_optimizer.step()

        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()

        self.actor_scheduler.step(policy_loss)
        self.critic_scheduler.step(critic_loss)

        for target_param, param in zip(self.actor_target.parameters(), self.actor.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))
       
        for target_param, param in zip(self.critic_target.parameters(), self.critic.parameters()):
            target_param.data.copy_(param.data * self.tau + target_param.data * (1.0 - self.tau))

    def get_action(self, state, t):
        final_move = 0
        # Exploration / Exploitation tradeoff
        if random.randint(0, 100) < self.epsilon:
            final_move = random.randint(0, 1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.actor(state0)
            final_move = torch.argmax(prediction).item()
        return final_move
    
    def save(self):
        self.actor.save(file_name="actor.pt")
        self.actor_target.save(file_name="actor-target.pt")

        self.critic.save(file_name="critic.pt")
        self.critic_target.save(file_name="critic-target.pt")

    def cat(self, list1, list2):
        res = []
        for l1, l2 in zip(list1, list2):
            l = []
            for i in l1:
                l.append(i)
            l.append(l2)
            res.append(l)
        return torch.Tensor(res)
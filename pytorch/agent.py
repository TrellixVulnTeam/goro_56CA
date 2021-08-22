import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from network import QNetwork

class BQN(nn.Module):
    def __init__(self,state_space : int, action_num : int,action_scale : int, learning_rate, device : str):
        super(BQN,self).__init__()

        self.q = QNetwork(state_space, action_num,action_scale).to(device)
        self.target_q = QNetwork(state_space, action_num,action_scale).to(device)
        self.target_q.load_state_dict(self.q.state_dict())

        self.optimizer = optim.AdamW([\
                                    {'params' : self.q.linear_1.parameters(), 'weight_decay':0.0001 ,'lr': learning_rate / (action_num+2)},\
                                    {'params' : self.q.linear_2.parameters(), 'weight_decay':0.0001,'lr': learning_rate / (action_num+2)},\
                                    {'params' : self.q.value.parameters(), 'weight_decay':0.0001, 'lr' : learning_rate/ (action_num+2)},\
                                    {'params' : self.q.actions.parameters(), 'weight_decay':0.0001, 'lr' : learning_rate},\
                                    ])  
        # self.optimizer = optim.Adam(self.q.parameters(), lr=learning_rate, weight_decay=0.0001)
        self.update_freq = 1000
        self.update_count = 0
    def action(self,x):
        return self.q(x)
    
    def save_model(self, name):
        torch.save({
                    'modelA_state_dict': self.q.state_dict(),
                    'modelB_state_dict': self.target_q.state_dict(),
                    'optimizerA_state_dict': self.optimizer.state_dict()
                    }, "./models/gem5model"+str(name))
        torch.save({
                    'modelA_state_dict': self.q.state_dict(),
                    'modelB_state_dict': self.target_q.state_dict(),
                    'optimizerA_state_dict': self.optimizer.state_dict()
                    }, "./gem5model_latest")
    
    def load_model(self):
        checkpoint = torch.load(("/home/ml/test/BipedalWalker-BranchingDQN/gem5model"))
        self.q.load_state_dict(checkpoint['modelA_state_dict'])
        
    def train_mode(self,n_epi,memory,batch_size,gamma,use_tensorboard,writer):
        state, actions, reward, next_state, done_mask = memory.sample(batch_size)
        
        # print("state", type(state), len(state), type(state[0]), state)
        # print("actions", type(actions), len(actions), type(actions[0]))
        # print("reward", type(reward), len(reward), type(reward[0]))
        # print("next_state", type(next_state), len(next_state), type(next_state[0]))
        # print("done_mask", type(done_mask), len(done_mask), type(done_mask[0]), done_mask)
 
        # input()
         
        
        actions = torch.stack(actions).transpose(0,1).unsqueeze(-1)
        done_mask = torch.abs(done_mask-1)
        
        cur_actions = self.q(state)
        cur_actions = torch.stack(cur_actions).transpose(0,1)
        cur_actions = cur_actions.gather(2,actions.long()).squeeze(-1)

        target_cur_actions = self.target_q(next_state)
        target_cur_actions = torch.stack(target_cur_actions).transpose(0,1)
        target_cur_actions = target_cur_actions.max(-1,keepdim = True)[0]
        # print("done_mask", done_mask)
        target_action = (done_mask * gamma * target_cur_actions.mean(1) + reward)

        # cur_actions = int(cur_actions)
        #
        loss = F.mse_loss(cur_actions,target_action.repeat(1,7))
        # target = target_action.repeat(1,7)
        # target = target.to(dtype=torch.long)
        # print("cur_actions", cur_actions)
        # print("target", target)
        # loss = F.cross_entropy(cur_actions, target)
        # loss = F.smooth_l1_loss(cur_actions,target_action.repeat(1,7))
        # loss = nn.CrossEntropyLoss()
        # loss = loss(cur_actions, target_action.repeat(1,7))
        
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.update_count += 1
        if (self.update_count % self.update_freq == 0) and (self.update_count > 0):
            # print("Updating the q net")
            self.update_count = 0
            self.target_q.load_state_dict(self.q.state_dict())
            
        # if use_tensorboard:
            # writer.add_scalar("Loss/loss", loss, n_epi)
        
        return loss

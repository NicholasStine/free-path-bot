# https://medium.com/@sthanikamsanthosh1994/reinforcement-learning-part-2-policy-gradient-reinforce-using-tensorflow2-a386a11e1dc6

import numpy as np
import tensorflow as tf
from network import PGNetwork

TEMP = 1.2

class Agent:
    def __init__(self, lr=0.0002, gamma=0.80, action_dim=4):
        self.gamma = gamma
        self.action_dim = action_dim
        
        self.states = []
        self.actions = []
        self.rewards = []
        
        self.policy = PGNetwork(action_dim)
        self.policy.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=lr))
        # self.policy.compile(optimizer = tf.keras.optimizers.Adam(learning_rate=lr), loss=lambda y_true, y_pred: -y_pred)
        
    def sample(self, state, j):
        state = tf.convert_to_tensor([state], dtype=tf.float32)
        action_probs = self.policy(state)
        
        scaled_logits = tf.math.log(action_probs) / TEMP
        action = tf.random.categorical(scaled_logits, num_samples=5)
        
        action = action.numpy()[0]
        hands = next(filter(lambda x: x == 0 or x == 1, action), -1)
        feet = next(filter(lambda x: x == 2 or x == 3, action), -1)
        # if (j % 100 == 0): print(action)
        return int(hands), int(feet)
    
    def store(self, state, action, reward):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        
    def learn(self):
        rewards = np.array(self.rewards)
        
        G = np.zeros_like(rewards)
        for t in range(len(rewards)):
            G_sum = 0
            discount = 1
            for k in range(t, len(rewards)):
                G_sum += rewards[k] * discount
                discount *= self.gamma
            G[t] = G_sum
            
        with tf.GradientTape() as tape:
            loss = 0
            for idx, (g, state) in enumerate(zip(G, self.states)):
                state = tf.convert_to_tensor([state], dtype=tf.float32)
                action_probs = self.policy(state)
                action = tf.random.categorical(tf.math.log(action_probs) / TEMP, num_samples=1)
                log_prob = tf.math.log(action_probs[0,action[0,0]])
                loss += -g * tf.squeeze(log_prob)
        
        print("Loss:",loss.numpy())
                
        gradient = tape.gradient(loss, self.policy.trainable_variables)
        self.policy.optimizer.apply_gradients(zip(gradient, self.policy.trainable_variables))
        
        self.states = []
        self.actions = []
        self.rewards = []
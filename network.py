# https://medium.com/@sthanikamsanthosh1994/reinforcement-learning-part-2-policy-gradient-reinforce-using-tensorflow2-a386a11e1dc6

from tensorflow import keras
from keras.layers import Dense

class PGNetwork(keras.Model):
    def __init__(self, action_dim):
        super(PGNetwork, self).__init__()
        self.dense0 = Dense(128, activation='relu')
        self.dense1 = Dense(128, activation='relu')
        self.pi = Dense(action_dim, activation='softmax')
        
    def call(self, state):
        x = self.dense0(state)
        x = self.dense1(x)
        return self.pi(x)

# from sillygoose import SillyGoose
from joystick import Joystick
import numpy as np
import tensorflow as tf
import random

class Network(tf.keras.Model):
    def __init__(self):
        super(Network, self).__init__()
        self.hidden1 = tf.keras.layers.Dense(8, activation='relu')
        self.hidden2 = tf.keras.layers.Dense(8, activation='relu')
        self.output_layer = tf.keras.layers.Dense(4, activation='sigmoid')
    
    def call(self, inputs):
        x = self.hidden1(inputs)
        x = self.hidden2(x)
        return self.output_layer(x).numpy()[0]

class Agent():
    def __init__(self, game, population_count, network=None):
        # self.dummy = SillyGoose()
        self.game = game
        self.population_count = population_count
        self.joystick = Joystick(game)
        self.network = network if network else Network()
        self.id = random.randint(1,99)
        print("id: ",self.id)
    
    def discretize_output(self, network_output):
        gas, brake, left, right = network_output
        hand_pics, feet_pics = self.joystick.sample()
        hands = 0 if left > 0.5 else 1 if right > 0.5 else -1
        feet = 2 if gas > 0.5 else 3 if brake > 0.5 else -1
        hands = max(hands, hand_pics)
        feet = max(feet, feet_pics) # Feet Pics? What? Me? Nooooo, I would never! ;D
        return hands, feet
    
    def sample(self, state):
        car_state = state[1:5]
        network_output = self.network(tf.convert_to_tensor([car_state]))
        return self.discretize_output(network_output)
        # return self.dummy.sample(state)
    
    def learn(self, population, rewards):
        print("learning")
        arg_sort = np.argsort(rewards)
        most_goodest_boys = [population[i] for i in arg_sort[:int(self.population_count * 0.2)]]
        
        new_goodest_boys = most_goodest_boys.copy()
        while len(new_goodest_boys) < self.population_count:
            parent1, parent2 = np.random.choice(most_goodest_boys, 2)
            child_network = self.crossover(parent1.network, parent2.network)
            child_network = self.mutate(child_network)
            child_agent = Agent(self.game, self.population_count, child_network)
            new_goodest_boys.append(child_agent)
            
        return new_goodest_boys
        
    
    def mutate(self, model):
        for layer in [model.hidden1, model.hidden2, model.output_layer]:
            if np.random.rand() < 0.1:
                noise = tf.random.normal(layer.weights[0].shape, 0, 0.1)
                layer.weights[0].assign_add(noise)
        return model
    
    def crossover(self, parent1, parent2):
        child = Network()
        child(tf.zeros((1,4), dtype=tf.float32))
        for p1, p2, c in [(parent1.hidden1, parent2.hidden1, child.hidden1),
                        (parent1.hidden2, parent2.hidden2, child.hidden2),
                        (parent1.output_layer, parent2.output_layer, child.output_layer)]:
            mask = np.random.rand(*p1.weights[0].shape) > 0.5
            print("C WEIGHTS: ", c.weights)
            c.weights[0].assign(tf.where(mask, p1.weights[0], p2.weights[0]))
            c.weights[1].assign((p1.weights[1] + p2.weights[1]) / 2)  # Bias avg
        return child
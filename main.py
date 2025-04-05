from game import Game
# from policyGradientAgent import Agent
from geneticFCAgent import Agent
from joystick import Joystick
import pygame

env = Game()
# agent = Agent()
joystick = Joystick(env)
# silly_goose = SillyGoose()

scores = []
generation_count = 100
population_count = 50

population = [Agent(env, population_count) for _ in range(population_count)]
# exit(0)

clock = pygame.time.Clock()

for g in range(generation_count):
    rewards = []
    for agent in population:
        done = False
        score = 0
        state = env.start()
        j = 0
        while not done:
            # hands, feet = agent.sample(state, j)
            # hands, feet = joystick.sample()
            hands, feet = agent.sample(state)
            state_, reward, done = env.step(hands, feet, clock)
            # agent.store(reward)
            state = state_
            score += reward
            j += 1
            if (j > 3000): done = True
        rewards.append(score)
        
    
    new_population = agent.learn(population, rewards)
    population = new_population
        
        
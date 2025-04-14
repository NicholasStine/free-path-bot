import pickle
from game import Game
# from policyGradientAgent import Agent
# from geneticFCAgent import Agent
from bresenham import Bresenham
from joystick import Joystick
import pygame

from ogm import OccupancyGrid

env = Game()
# agent = Agent()
joystick = Joystick(env)
# silly_goose = SillyGoose()

scores = []
generation_count = 30
population_count = 35

# population = [Agent(env, population_count) for _ in range(population_count)]
# exit(0)

clock = pygame.time.Clock()

ogm_observations = []
bressie = Bresenham(env.track_size)
for g in range(generation_count):
    rewards = []
    # for agent in population:
    for i in range(population_count):
        done = False
        score = 0
        state = env.start()
        j = 0
        while not done:
            # hands, feet = agent.sample(state, j)
            hands, feet = joystick.sample()
            # hands, feet = agent.sample(state)
            state_, reward, done = env.step(hands, feet, clock)
            ogm_observations.append([(env.car.x, env.car.y, env.car.theta), env.car.lidar.observations])
            # ogm_observations.append([(env.car.x, env.car.y, env.car.theta), [
            #     env.car.scanner.far_left.last_end, 
            #     env.car.scanner.out_left.last_end, 
            #     env.car.scanner.in_left.last_end, 
            #     env.car.scanner.forward_left.last_end, 
            #     env.car.scanner.forward.last_end, 
            #     env.car.scanner.forward_right.last_end, 
            #     env.car.scanner.in_right.last_end, 
            #     env.car.scanner.out_right.last_end,
            #     env.car.scanner.far_right.last_end
            # ]])
            # agent.store(reward)
            state = state_
            score += reward
            j += 1
            if (j > 3000): done = True
        bresenham_score = bressie.evaluate(ogm_observations, env.car.lidar.angles)
        print(bresenham_score)
        rewards.append(bresenham_score)
        # rewards.append(score)
        # try:
        # except error:
            # print(error)
        # print(len(ogm_observations))
        ogm_observations = []
        bressie.reset()
        # print(len(ogm_observations))
        
    
    # new_population = agent.learn(population, rewards)
    # population = new_population

with open('latest_ogm_observations', 'wb') as pickle_file:
    pickle.dump(ogm_observations, pickle_file)
# angles = [0, 45, -45]
# grid = OccupancyGrid(env.track_size[1], env.track_size[0], 10.0)
# for (x, y, theta), ranges in ogm_observations:
#     grid.update(x, y, theta, ranges, angles)
#     # print(trajectory)
#     # print(scans, '\n')
    
# grid.plot_grid()
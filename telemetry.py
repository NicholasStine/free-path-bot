import pygame

class Telemetry():
    def __init__(self, screen, track, car):
        self.screen = screen
        self.track = track
        self.car = car
        
        self.car_theta = 0
        self.car_velocity = 0
        self.path_length = 0
        self.left_length = 0
        self.right_length = 0
        self.steering_change = 0
        self.lambda_smooth = 1
        
        self.on_track = True
        self.checkpoint = False
        self.finished = False
        
        self.time_reward = 0
        self.path_reward = 0
        self.velocity_reward = 0
        self.braking_reward = 0
        self.previous_velocity = 0
        self.smooth_operator_reward = 0
        self.prev_theta = 0
        self.movement_reward = 0
        self.travel_reward = 0
        
        self.score = 0
        self.time_step = 0
        
    def blit(self):
        pygame.draw.rect(self.screen, (100,100,100 + 155 * self.car_theta), pygame.Rect(60,0,30,30))
        pygame.draw.rect(self.screen, (100,100,100 + 155 * self.car_velocity), pygame.Rect(120,0,30,30))
        pygame.draw.rect(self.screen, (100,100,100 + 155 * self.path_length), pygame.Rect(180,0,30,30))
        
        pygame.draw.rect(self.screen, (100,100,255 if self.on_track else 100), pygame.Rect(240,0,30,30))
        pygame.draw.rect(self.screen, (100,100,255 if self.checkpoint else 100), pygame.Rect(300,0,30,30))
        pygame.draw.rect(self.screen, (100,100,255 if self.finished else 100), pygame.Rect(360,0,30,30))
    
    def reset(self):
        self.time_step = 0
    
    def getAll(self, car_pos):
        combined = *self.getCarTel(), *self.getTrackTel(car_pos)
        self.prev_theta = self.car_theta
        return combined
    
    def getCarTel(self):
        self.car_theta = self.car.theta / 360
        self.car_velocity = min(1, self.car.velocity * 1.2)
        self.path_length = self.car.scanner.forward.last_end / self.car.scanner.MAX_LEN
        self.left_length = self.car.scanner.far_left.last_end / self.car.scanner.MAX_LEN
        self.right_length = self.car.scanner.far_right.last_end / self.car.scanner.MAX_LEN
        self.steering_change = self.car.theta_delta
        self.travel_dist = self.car.travel_dist
        # return self.path_length, self.left_length, self.right_length, self.car_velocity
        return self.car_theta, self.car_velocity, self.path_length, self.left_length, self.right_length, self.steering_change, self.travel_dist
    
    def getTrackTel(self, car_pos):
        self.on_track = self.track.getOnTrack(car_pos)
        self.finished = self.track.getPassedFinish(car_pos)
        self.checkpoint = self.track.getPassedCheckpoint(car_pos)
        return self.on_track, self.finished, self.checkpoint
    
    def printMax(self):
        # pass
        print("time_reward:",self.time_reward)
        print("path_reward:",self.path_reward)
        print("velocity_reward:",self.velocity_reward)
        print("braking_reward:",self.braking_reward)
        print("smooth_operator_reward:",self.smooth_operator_reward)
        print("travel_reward:",self.travel_reward)
    
    def newGetReward(self):
        # the reward funciton needs to use the lasers!
        # greatest average path:
        #   reward turning towards
        #   penalize turning away
        # left right average:
        #   reward turns that increase average
        #   penalize rewards that decrease average
        pass
    
    def getReward(self, stuck):
        self.time_step += 1
        
        return 0 if stuck else self.car_velocity * 5 + self.path_length * 10 + self.left_length * 3 + self.right_length * 3 
        
        # target_direction = (self.car.theta - target_theta) / 45
        # car_direction = self.car.theta_delta / 2
        
        # steering_reward = -abs(car_direction - target_direction)
        # if (self.time_step % 50 == 0):
            # print("car_direction:",car_direction)
            # print("target_direction:",target_direction)
            # print(steering_reward)
        # return steering_reward
        time_reward = self.time_step / 3000
        path_reward = (self.path_length + self.left_length + self.right_length) / (self.car.scanner.MAX_LEN * 3)
        velocity_reward = self.car_velocity * path_reward * 2
        braking_reward = (self.previous_velocity - self.car_velocity) / (path_reward * 3000)
        self.previous_velocity = self.car_velocity
        smooth_operator_reward = (self.lambda_smooth * self.steering_change) / (path_reward * 10000)
        travel_reward = self.travel_dist / 10000
        
        self.time_reward += time_reward
        self.path_reward += path_reward
        self.velocity_reward += velocity_reward
        self.braking_reward += braking_reward
        self.smooth_operator_reward += smooth_operator_reward
        self.travel_reward += travel_reward
        
        return time_reward + path_reward + velocity_reward + braking_reward + travel_reward + smooth_operator_reward
import math
import random
import pygame
from lidar import Lidar
from scanner import Scanner

START_X = 100
START_Y = 130
START_T = 270
START_V = 0.2
STARTS = [(330,30,270), (380, 410, 270)]
# STARTS = [(10,85,270), (560,125,290), (1345,80,90)]

class Car():
    def __init__(self, screen, track):
        self.ROTATION_SPEED = 1.8
        self.screen = screen
        self.x = START_X
        self.y = START_Y
        self.start_x = START_X
        self.start_y = START_Y
        self.theta = START_T
        self.theta_delta = 0
        self.velocity = START_V
        
        self.sprite = pygame.image.load('images/blue_race_car.png')
        self.sprite = pygame.transform.scale_by(self.sprite, 0.5)
        self.sprite_center = (self.sprite.get_width() / 2, self.sprite.get_height() / 2)
        self.lidar = Lidar(screen, track)
        self.scanner = Scanner(screen, track)
        
        self.travel_i = 0
        self.travel_dist = 0
        
    def reset(self):
        start = STARTS[0]
        # start = STARTS[random.randint(0,2)]
        self.x = start[0]
        self.y = start[1]
        self.start_x = start[0]
        self.start_y = start[1]
        self.theta = start[2] + random.uniform(-20,20)
        self.theta_delta = 0
        self.velocity = random.uniform(0.3,1.6)
        self.travel_i = 0
        self.travel_dist = 0
        
    def blit(self):
        self.screen.blit(self._rotate(self.sprite, self.theta), (self.x, self.y))
    
    def _move(self, velocity=None, offset=0):
        rad_bro = -(self.theta + offset) * (math.pi / 180) - math.pi / 2
        x = self.x + (velocity or self.velocity) * math.cos(rad_bro)
        y = self.y + (velocity or self.velocity) * math.sin(rad_bro)
        return x, y
    
    def move(self):
        x, y = self._move()
        self.x = x
        self.y = y
        self.updateTravel()
        return (int(self.x + self.sprite_center[0]), int(self.y + self.sprite_center[1]))
        
    def accelerate(self, d_velocity=0.006):
        self.velocity = min(self.velocity + d_velocity, 2)
        
    def brake(self, d_velocity=0.0025):
        self.deccelerate(d_velocity)
        
    def deccelerate(self, d_velocity=0.001):
        self.velocity = max(self.velocity - d_velocity, 0)
    
    def _rotate(self, surface, theta):
        # https://www.pygame.org/wiki/RotateCenter?parent=CookBook
        # Upped canvas size in gimp from 80x80 to 125x125 with transparent dots to maintain image width/height
        rotated_surface = pygame.transform.rotate(surface, theta)
        rotated_rect = surface.get_rect().copy()
        rotated_rect.center = rotated_surface.get_rect().center
        rotated_surface = rotated_surface.subsurface(rotated_rect).copy()
        return rotated_surface
        
    def updateTravel(self):
        self.travel_dist = abs(self.start_x - self.x) + abs(self.start_y - self.y)
        
    def checkStuck(self, start=100, threshold=0.3):
        self.travel_i += 1
        if (self.travel_i > start and self.travel_i % 10 == 0):
            return False
            # return self.velocity < threshold and (self.theta_delta > 1 or self.theta_delta < 0.1)
        return False
    
    # Rotate according to speed (pseudo continuously)
    def rotate(self, d_theta=0):
        rotation_factor = 1
        if (self.velocity == 0): return # if the car ain't movin, it ain't turnin, ya heard?
        else: rotation_factor = 3 / (self.velocity*5) + 0.03 # reduce the ability to turn in direct-ish proportion to the car's velocity
        rotation_factor = min(rotation_factor,0.7)
        new_theta = self.theta + d_theta * self.ROTATION_SPEED * rotation_factor
        self.theta_delta = self.theta - new_theta
        self.theta = 0 if new_theta > 360 else 360 if new_theta < 0 else new_theta
        
    # ray trace until color change, then break and draw laser
    def rayCast(self, on_track):
        self.lidar.cast(self, on_track)
        return 'poop smells stanky'
        # return self.scanner.cast(self, on_track)
        
        
import math
from laser import Laser

MAX_LEN = 500

class Scanner():
    def __init__(self, screen, track):
        self.forward = Laser(screen, track)
        self.left = Laser(screen, track, 45)
        self.right = Laser(screen, track, -45)
        self.MAX_LEN = MAX_LEN
        
    def cast(self, car, on_track):
        greatest_dist = 0
        target_angle = car.theta
        for i, laser in enumerate([self.forward, self.left, self.right]):
            dist = laser.cast(car, on_track)
            if (dist > greatest_dist):
                target_angle = car.theta + laser.offset
                target_i = i
                greatest_dist = dist
                
        direction_strings = ['forward', 'left', 'right']
        return target_angle
            

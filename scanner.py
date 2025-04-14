import math
from laser import Laser

MAX_LEN = 500

class Scanner():
    def __init__(self, screen, track):
        self.far_left = Laser(screen, track, 60)
        self.out_left = Laser(screen, track, 45)
        self.in_left = Laser(screen, track, 30)
        self.forward_left = Laser(screen, track, 15)
        self.forward = Laser(screen, track, 0)
        self.forward_right = Laser(screen, track, -15)
        self.in_right = Laser(screen, track, -30)
        self.out_right = Laser(screen, track, -45)
        self.far_right = Laser(screen, track, -60)
        self.MAX_LEN = MAX_LEN
        
    def cast(self, car, on_track):
        greatest_dist = 0
        target_angle = car.theta
        for i, laser in enumerate([
            self.far_left,
            self.out_left,
            self.in_left,
            self.forward_left,
            self.forward,
            self.forward_right,
            self.in_right,
            self.out_right,
            self.far_right
        ]):
            dist = laser.cast(car, on_track)
            if (dist > greatest_dist):
                target_angle = car.theta + laser.offset
                target_i = i
                greatest_dist = dist
                
        direction_strings = ['forward', 'left', 'right']
        return target_angle
            

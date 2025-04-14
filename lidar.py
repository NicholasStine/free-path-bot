# psst, come closer, I have to tell you a secret :)
# this isn't actually lidar! I'm totally cheating
# and just using a fixed set of lasers arranged from
# 0 to 360 - n, in steps of n degrees. I don't have
# to deal with a rotating laser, rotational drift, 
# positional drift. You ask the lidar class for a
# scan, and BOOM, you get an instantaneous snapshot
# of all distances.

# Cheeky, I know, I know. But I've hit a wall with
# using OGM to calculate reward for area covered, 
# because without lasers pointing in all directions,
# the current configuration of measuring from -180
# to 180 deg actually rewards the car for turning in
# circles, since turning around allows the lasers to 
# measure more environment area, thus returning a
# greater reward. With lasers emitting in all 
# directions, I'm hoping that I can make a reward
# function that only rewards exploring new positions
# and exploring new angles will provide little to no
# additional reward.


from laser import Laser

THETA_STEP = 12

class Lidar():
    def __init__(self, screen, track):
        self.lasers = []
        self.angles = []
        self.observations = []
        for laser_theta in range(int(360/THETA_STEP)):
            theta = laser_theta * THETA_STEP
            self.lasers.append(Laser(screen, track, theta))
            self.angles.append(theta)
            
    def cast(self, car, on_track):
        self.observations = []
        for laser in self.lasers:
            dist = laser.cast(car, on_track)
            self.observations.append(dist)
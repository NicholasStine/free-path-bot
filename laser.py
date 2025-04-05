import pygame

class Laser():
    def __init__(self, screen, track, offset=0):
        self.screen = screen
        self.track = track
        self.offset = offset
        self.last_end = 0
        self.MAX_LEN = 500
        
    def cast(self, car, on_track):
        start = (int(car.x + car.sprite_center[0]), int(car.y + car.sprite_center[1]))
        ray_point = (int(car.x + car.sprite_center[0]), int(car.y + car.sprite_center[1]))
        end = None
        cacumulations = 0
        for ray_n in range(self.MAX_LEN):
            cacumulations += 1
            try:
                ray_n0 = self.track.sprite.get_at(ray_point)
                ray_point = car._move(ray_n, self.offset) 
                ray_point = (int(ray_point[0] + car.sprite_center[0]), int(ray_point[1] + car.sprite_center[1]))
                compare_color = (255,255,255) if on_track else (0,0,0)
                if (ray_n0[:3] == compare_color):
                    self.last_end = ray_n # track last n at which ray trace ended
                    end = ray_point
                    break
            except IndexError as err:
                pass
            
        color_factor = int((self.last_end or 1) / 5)
        LASER_caution = (255-color_factor,100+color_factor,100) if on_track else (100,255,0)
        if (end): pygame.draw.line(self.screen, LASER_caution, start, end)
        return self.last_end

# what does a track do?
# a track does what a track needs to do,
# because a track is a man;
# and that's what a man does.

#    - Gus Fring

# I've got a 

import pygame

class Track():
    def __init__(self, screen, sprite):
        self.screen = screen
        self.sprite = sprite
    
    def blit(self):
        self.screen.blit(self.sprite, (0, 0))
        
    def getPixelColor(self, pos):
        try:
            return self.sprite.get_at(pos)
        except IndexError:
            return (255, 255, 255, 0)
    
    def getOnTrack(self, car_pos):
        pixel_color = self.getPixelColor(car_pos)
        return pixel_color[:3] != (255,255,255)
        
    def getPassedFinish(self, car_pos):
        pixel_color = self.getPixelColor(car_pos)
        return pixel_color[1] > 100 and pixel_color[2] < 100
        
    def getPassedCheckpoint(self, car_pos):
        pixel_color = self.getPixelColor(car_pos)
        return pixel_color[2] > 200 and pixel_color[1] < 200
    
    def getCollisions(self):
        pass
    
    def getProgress(self):
        pass
    
    def getLapTime(self):
        pass


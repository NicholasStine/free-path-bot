import pygame

class Joystick():
    def __init__(self, game):
        self.game = game
        
    def sample(self):
        keypress = pygame.key.get_pressed()
        hands = -1
        feet = -1
        
        hands = 0 if keypress[pygame.K_LEFT] else 1 if keypress[pygame.K_RIGHT] else -1
        feet = 2 if keypress[pygame.K_UP] else 3 if keypress[pygame.K_DOWN] else -1
                
        return hands, feet
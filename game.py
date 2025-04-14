import pygame
from car import Car
from track import Track
from telemetry import Telemetry

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Path Finding')
        
        track_sprite = pygame.image.load('images/daytona.jpg')
        track_size = track_sprite.get_size()
        self.track_size = track_size
        
        self.screen = pygame.display.set_mode((track_size[0], track_size[1]))

        self.track = Track(self.screen, track_sprite)
        self.car = Car(self.screen, self.track)
        self.telemetry = Telemetry(self.screen, self.track, self.car)
        self.on_track = True
        self.finished = False
        
    def sandbox(self):
        left_clicked = self.checkQuit()
        self.screen.fill((255,255,255))
        self.track.blit()
        return left_clicked
        
    def start(self):
        self.telemetry.reset()
        self.car.reset()
        return self.step()[0]
        
    def play(self):
        self.start()
                
    def checkQuit(self):
        left_clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                left_clicked = True
        return left_clicked
                
    def printMax(self):
        self.telemetry.printMax()

    def step(self, hands=None, feet=None, clock=None):
        self.screen.fill((255,255,255))
        
        # Let our robot overlord take the wheel
        key_rotate = 1 if hands == 0 else -1 if hands == 1 else 0
        self.car.rotate(key_rotate)
        
        if (feet == 2):
            self.car.accelerate()
        elif (feet == 3):
            self.car.brake()
        else:
            self.car.deccelerate()
        
        car_pos = self.car.move()
        self.telemetry.getCarTel()
        on_track, finished, checkpoint = self.telemetry.getTrackTel(car_pos)
        indicator = (255,0,0) if not on_track else (0,255,0) if finished and on_track else (200,200,255) if checkpoint and on_track else (0,0,255)
        
        self.track.blit()
        self.car.blit()
        target_theta = self.car.rayCast(on_track)
        pygame.draw.rect(self.screen, indicator, pygame.Rect(0, 0, 30, 30))
        pygame.display.flip()
        # pygame.time.wait(100)
        if (clock): clock.tick(100)
        self.checkQuit()
        stuck = self.car.checkStuck()
        return self.telemetry.getAll(car_pos), self.telemetry.getReward(stuck), (not on_track) or finished or stuck

if __name__ == '__main__':
    game = Game()
    game.play()
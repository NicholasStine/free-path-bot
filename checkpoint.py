from game import Game
from checkpointPhysics import checkpointCrossed
import pygame
import pickle
import sys
import os

clear_pickle = '--clear' in sys.argv[1:]
check_crossed = '--crossed' in sys.argv[1:]

if (__name__ == '__main__'):
    
    pygame.font.init()
    text = pygame.font.SysFont('Comic Sans MS', 20)
    
    game = Game()
    pairs = []
    crossed_pairs = []
    
    try:
        if (clear_pickle):
            os.remove('ofofofof')
            
        with open('ofofofof', 'rb') as pickle_file:
            saved_pairs = pickle.load(pickle_file)
            pairs = saved_pairs
            
    except FileNotFoundError:
        print('No Pickle File Found')
    
    while (True):
        left_clicked = game.sandbox()
        mouse_pos = pygame.mouse.get_pos()
        
        if (left_clicked):
            pairs.append(mouse_pos)
            
        for n, pair in enumerate((pairs[n:n+2] for n in range(0, len(pairs), 2)), 1):
            pygame.draw.circle(game.screen, (255, 100, 100), pair[0], 5)
            
            if (len(pair) == 2):
                number = text.render(f'{n}', False, (64, 224, 208))
                game.screen.blit(number, pair[1])
                
                crossed = checkpointCrossed(mouse_pos, pair[0], pair[1]) if check_crossed else False
                if (crossed):
                    print("SHIT!!!")
                    crossed_pairs.append(n)
                    break
                
                else:
                    pygame.draw.circle(game.screen, (100, 100, 255), pair[1], 5)
                    pygame.draw.line(game.screen, (255, 90, 180) if crossed else (255, 255, 255) if n == int(len(pairs) / 2) else (100, 255, 100), pair[0], pair[1])
                
        
        print(crossed_pairs)
            
        if not check_crossed:
            with open('ofofofof', 'wb') as pickle_file:
                pickle.dump(pairs, pickle_file)
            
        pygame.display.flip()


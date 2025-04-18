from math import radians, sin, cos
import pickle

import scipy.ndimage as murfurlurgy
from matplotlib import pyplot as plt, cm
import numpy as np

# Sensor model parameters
LOG_ODDS_OCCUPIED = np.log(0.9 / 0.1)  # Positive update for occupied
LOG_ODDS_FREE = np.log(0.5 / 0.9)      # Negative update for free

CELL_SIZE = 10
class Bresenham():
    def __init__(self, track_size):
        track_width, track_height = track_size
        self.track_width = track_width
        self.track_height = track_height
        self.grid = [[LOG_ODDS_OCCUPIED]*(int(track_width/CELL_SIZE)) for i in range(int(track_height/CELL_SIZE))]
    
    def reset(self):
        self.grid = [[LOG_ODDS_OCCUPIED]*(int(self.track_width/CELL_SIZE)) for i in range(int(self.track_height/CELL_SIZE))]
    
    def evaluate(self, observations, angles=None):
        default_angles = [60, 45, 30, 15, 0, -15, -30, -45, -60]
        laser_angles = angles if angles else default_angles
        score = 0
        for car_data, scanner_data in observations[:]:
            car_x, car_y, car_theta = car_data
            for i, scan in enumerate(scanner_data):
                laser_theta = 360 - (car_theta + laser_angles[i] + 90)
                laser_theta = laser_theta - 360 if laser_theta > 360 else laser_theta
                score += self.scanToCoord(car_x, car_y, scan, laser_theta)
                
        # print("SCORE: ", score)
        self.plot()
        return score

    def plot(self):
        np_grid = np.array(self.grid, dtype="float32")
        
        plt.imshow(np_grid, cmap='cool', origin='upper')
        plt.colorbar(label='Occupancy Probability')
        plt.title('Occupancy Grid Map')
        plt.show()
        
        # print
        np_track = np.where(np_grid < 0.005, 1.0, 0.0)
        np_edges = np.where(np_grid > 3, 1.0, 0.0)
        
        # Just a wee bit of murrfurrlurrgyy to pad the
        # detected edges, and denoise the track and edge
        # readings! In some way I don't understand, 
        # dilating the edges seems to successfully remove
        # weird artifacts that I get between the track
        # and edges when I don't include dilation.. very strange stuff!
        np_track = murfurlurgy.binary_erosion(np_track, iterations=2).astype(np_track.dtype)
        np_edges = murfurlurgy.binary_dilation(np_edges, iterations=2).astype(np_edges.dtype)
        
        # Draws white for track, and black for padded edges and occupied cells.
        safe_zone = np.stack([np_track - np_edges, np_track, np_track], axis=-1).astype(np_track.dtype)
        final_img = safe_zone
        
        plt.imshow(final_img, cmap='cool', origin='upper')
        plt.colorbar(label='Occupancy Probability')
        plt.title('Occupancy Grid Map')
        plt.show()
        
        # Draws red for edges and white for the track
        colored_track = np.stack([np_track + np_edges, np_track, np_track], axis=-1)
        final_img = colored_track
        
        plt.imshow(final_img, cmap='cool', origin='upper')
        plt.colorbar(label='Occupancy Probability')
        plt.title('Occupancy Grid Map')
        plt.show()

    def scanToCoord(self, x, y, distance, theta):
        """ Convert car x, y and laser scan distance, theta
            to grid (integer) start and end coordinates
            (x0, y0), (x1, y1)
        """
        end_x = int(x + distance * cos(radians(theta)))
        end_y = int(abs(y + distance * sin(radians(theta))))
        end_x = int(end_x / CELL_SIZE)
        end_y = int(end_y / CELL_SIZE)
        x = int(x / CELL_SIZE)
        y = int(y / CELL_SIZE)
        
        score = 0
        for line_x, line_y in self.bresenham(x, y, end_x, end_y):
            try:
                self.grid[line_y][line_x] += LOG_ODDS_FREE
                val = self.grid[line_y][line_x]
                # print(val)
                score -= -0.0001 if val < -1 else val * 0.00001
            except IndexError:
                pass
        try: 
            self.grid[end_y][end_x] += LOG_ODDS_OCCUPIED
            score -= 0.01
        except IndexError:
            pass
        
        return abs(score)

    def bresenham(self, x0, y0, x1, y1):
        """Yield integer coordinates on the line from (x0, y0) to (x1, y1).

        Input coordinates should be integers.

        The result will contain both the start and the end point.
        """
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2*dy - dx
        y = 0

        for x in range(dx + 1):
            if D >= 0:
                y += 1
                D -= 2*dx
            D += 2*dy
            yield x0 + x*xx + y*yx, y0 + x*xy + y*yy

# if __name__ == '__main__':
#     with open('latest_ogm_observations', 'rb') as pickle_file:
#         observations = pickle.load(pickle_file)
#     evaluate(observations)
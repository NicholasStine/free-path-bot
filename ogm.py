import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, radians

# Grid parameters
GRID_SIZE = 50  # 20x20 grid
CELL_SIZE = 1.0  # 1 meter per cell
LOG_ODDS_PRIOR = 0.0  # Initial log-odds (P=0.5)

# Sensor model parameters
LOG_ODDS_OCCUPIED = np.log(0.9 / 0.1)  # Positive update for occupied
LOG_ODDS_FREE = np.log(0.1 / 0.9)      # Negative update for free

class OccupancyGrid:
    def __init__(self, game_width, game_height, cell_size_pixels):
        self.cell_size = cell_size_pixels
        self.grid_width = int(np.ceil(game_width / cell_size_pixels))
        self.grid_height = int(np.ceil(game_height / cell_size_pixels))
        self.log_odds = np.full((self.grid_height, self.grid_width), LOG_ODDS_PRIOR, dtype=float)
        self.game_width = game_width
        self.game_height = game_height

    def world_to_grid(self, x, y):
        gx = int(x / self.cell_size)
        gy = int((self.game_height - y) / self.cell_size)  # Flip y-axis for top-left origin
        return gx, gy

    def is_valid(self, gx, gy):
        return 0 <= gx < self.grid_width and 0 <= gy < self.grid_height

    def bresenham(self, x0, y0, x1, y1):
        """Bresenham's line algorithm to get cells along a beam."""
        cells = []
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            cells.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy
        return cells

    def update(self, robot_x, robot_y, robot_theta, ranges, angles):
        """Update the grid with a laser scan."""
        rx, ry = self.world_to_grid(robot_x, robot_y)
        for r, theta in zip(ranges, angles):
            # Calculate endpoint of the beam in world coordinates
            beam_angle = robot_theta + theta
            bx = robot_x + r * cos(radians(beam_angle))
            by = robot_y + r * sin(radians(beam_angle))
            ex, ey = self.world_to_grid(bx, by)

            # Get cells along the beam
            if self.is_valid(rx, ry) and self.is_valid(ex, ey):
                cells = self.bresenham(rx, ry, ex, ey)
                # Update free cells (all but the last)
                for gx, gy in cells[:-1]:
                    if self.is_valid(gx, gy):
                        self.log_odds[gx, gy] += LOG_ODDS_FREE
                # Update occupied cell (endpoint)
                if self.is_valid(ex, ey):
                    self.log_odds[ex, ey] += LOG_ODDS_OCCUPIED

    def get_probabilities(self):
        """Convert log-odds to probabilities."""
        return 1 / (1 + np.exp(-self.log_odds))
    
    # Visualize the result
    def plot_grid(self):
        probs = self.get_probabilities()
        plt.imshow(probs, cmap='gray', origin='upper')
        plt.colorbar(label='Occupancy Probability')
        plt.title('Occupancy Grid Map')
        plt.xlabel('X (cells)')
        plt.ylabel('Y (cells)')
        plt.show()

# Simulate a robot moving and scanning
# def simulate_mapping():
#     grid = OccupancyGrid(GRID_SIZE, CELL_SIZE)
    
#     # Simulated robot trajectory and scans
#     trajectory = [
#         (0.0, 0.0, 0.0),    # (x, y, theta in degrees)
#         (2.0, 0.0, 3.0),
#         (2.0, 2.0, 10.0),
#     ]
#     # Simple laser scan: 3 beams at -45°, 0°, 45°
#     angles = [-45, 0, 45]
    
#     # Simulated ranges for each position (meters)
#     SCAN_SCALE = 1
#     scans = [
#         [SCAN_SCALE+2.0, SCAN_SCALE+3.0, SCAN_SCALE+2.0],  # Obstacles at 2m, 3m, 2m
#         [SCAN_SCALE+3.0, SCAN_SCALE+4.0, SCAN_SCALE+3.0],
#         [SCAN_SCALE+2.0, SCAN_SCALE+5.0, SCAN_SCALE+2.0],
#     ]

#     # Update grid with each scan
#     for (x, y, theta), ranges in zip(trajectory, scans):
#         grid.update(x, y, theta, ranges, angles)

#     return grid


# Run the simulation
# if __name__ == "__main__":
    # grid = simulate_mapping()
    # grid.plot_grid()
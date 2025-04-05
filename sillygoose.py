

import random


class SillyGoose():
    def __init__(self):
        pass
    
    def sample(self, state):
        strait, left, right = state[2:5]
        
        # This big silly goose uses a heuristic ruleset to decide steering actions:
        # 1. left:      If on a strait and near a right edge
        # 2. right:     If on a strait and near a left edge
        # 3. strait:    If the strait distance is greater than the average side clearance
# CRASHY  4. fixed:     If the strait distance is near an edge, and the left and right distances are roughly equal
        # 5. right:     If the left distance is greater than the right distance
        # 6. left:      If the right distance is greater than the left distance
        
        go_strait = strait * 0.5 > (left + right) / 2
        avoid_right = right < 0.2 and strait > 0.3
        avoid_left = left < 0.2 and strait > 0.3
        avoid_outcrop = abs(right - left) < 0.2 and strait < 0.2
        longest_direction = 'left' if avoid_right else 'right' if avoid_left else 'strait' if go_strait else 'right' if avoid_outcrop else 'left' if left > right else 'right'
        
        return -1 if longest_direction == 'strait' else 0 if longest_direction == 'left' else 1, 2 if random.random() > 0.7 else 3
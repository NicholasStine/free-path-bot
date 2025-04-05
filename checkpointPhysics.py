

def checkpointCrossed(point, start, end, tolerance=20):
    """
    Check if a point lies on the line segment between start and end points.
    
    Args:
        point: tuple (x, y) - point to check
        start: tuple (x, y) - line segment start
        end: tuple (x, y) - line segment end
        tolerance: float - acceptable error margin
    
    Returns:
        bool - True if point lies on segment, False otherwise
    """
    px, py = point
    x1, y1 = start
    x2, y2 = end
    
    # Step 1: Check if point is within bounding box
    if not (min(x1, x2) - tolerance <= px <= max(x1, x2) + tolerance and
            min(y1, y2) - tolerance <= py <= max(y1, y2) + tolerance):
        return False
    
    # Step 2: Calculate distances
    # Distance between start and end (segment length)
    seg_length_squared = (x2 - x1)**2 + (y2 - y1)**2
    
    # If start and end are the same point
    if seg_length_squared == 0:
        return abs(px - x1) < tolerance and abs(py - y1) < tolerance
    
    # Step 3: Project point onto line using dot product
    # t is the projection factor (0 to 1 if point is on segment)
    t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / seg_length_squared
    if t < 0 or t > 1:
        return False
    
    # Step 4: Check distance from point to projected point
    # Calculate closest point on line
    closest_x = x1 + t * (x2 - x1)
    closest_y = y1 + t * (y2 - y1)
    
    # Distance from point to closest point on line
    dist_squared = (px - closest_x)**2 + (py - closest_y)**2
    
    return dist_squared <= tolerance * tolerance
def direct_path(start, finish, speed):
    """Computes the direct path between two (x, y) coordinates.
    
    It takes three arguments: `start`, `finish`, and `speed`. Both `start` 
    and `finish` are (x,y) tuples (representing Cartesian coordinates) 
    and `speed` is an int. The function returns a list of (x,y) tuples
    representing the direct path between `start` and `finish`, going by
    steps of size `speed`.  If you examine the example function calls,
    you will notice that this function takes care of an important detail:
    it doesn't overshoot the destination.

    Examples:

    >>> direct_path((1,1), (1,5), 2)
    [(1.0, 1.0), (1.0, 3.0), (1.0, 5.0)]
    >>> direct_path((7,13), (7,3), 5)
    [(7.0, 13.0), (7.0, 8.0), (7.0, 3.0)]
    >>> direct_path((2,2), (8,10), 5)
    [(2.0, 2.0), (5.0, 6.0), (8.0, 10.0)]
    >>> direct_path((1,1), (1,6), 2)
    [(1.0, 1.0), (1.0, 3.0), (1.0, 5.0), (1.0, 6.0)]
    """
    if start == finish:
        return [start]
    x1, y1 = start
    x2, y2 = finish
    distance = ((x1 - x2)**2 + (y1 - y2)**2)**.5
    step_factor = speed / (((x2-x1)**2 + (y2-y1)**2))**.5
    delta_x = (x2-x1) * step_factor
    delta_y = (y2-y1) * step_factor
    path = [(x1 + i * delta_x, y1 + i * delta_y) 
            for i in range(int(1 + distance/speed))]
    if len(path) == 0 or path[-1] != (x2, y2):
        path.append((x2, y2))
    return [(float(c[0]), float(c[1])) for c in path]
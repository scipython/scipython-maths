import numpy as np
from scipy.optimize import brentq

def intersection_area(d, R, r):
    """Return the area of intersection of two circles.

    The circles have radii R and r, and their centres are separated by d.

    """

    if d <= abs(R-r):
        # One circle is entirely enclosed in the other.
        return np.pi * min(R, r)**2
    if d >= r + R:
        # The circles don't overlap at all.
        return 0

    r2, R2, d2 = r**2, R**2, d**2
    alpha = np.arccos((d2 + r2 - R2) / (2*d*r))
    beta = np.arccos((d2 + R2 - r2) / (2*d*R))
    return ( r2 * alpha + R2 * beta -
             0.5 * (r2 * np.sin(2*alpha) + R2 * np.sin(2*beta))
           )

def find_d(A, R, r):
    """
    Find the distance between the centres of two circles giving overlap area A.

    """

    # A cannot be larger than the area of the smallest circle!
    if A > np.pi * min(r, R)**2:
        raise ValueError("Intersection area can't be larger than the area"
                         " of the smallest circle")
    if A == 0:
        # If the circles don't overlap, place them next to each other
        return R+r

    if A < 0:
        raise ValueError('Negative intersection area')

    def f(d, A, R, r):
        return intersection_area(d, R, r) - A

    a, b = abs(R-r), R+r
    d = brentq(f, a, b, args=(A, R, r))
    return d

r, R = 0.5, 1.5
A = np.pi * r**2
print(intersection_area(1, R, r) / A)
print(intersection_area(np.sqrt(2), R, r) / A)

import numpy as np
import scipy.optimize as op

def perp_error(plane, points):
    a, b, c, d = plane
    distance = 0;
    for point in points:
        x,y,z = point
        distance = distance + (a * x + b * y + c * z + d)**2 / (a**2 + b**2 + c**2)**(0.5)
    return distance

def objective(x,*args):
    puntos = args[0]
    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    f = []
    for punto in puntos:
        x, y, z = punto
        f.append((a * x + b * y + c * z + d)**2 / (a ** 2 + b ** 2 + c ** 2) ** (0.5))
    return sum(f)


points = [(-0.07111297, 0.06275147, 0.00879955), (-0.07511501, 0.06655704, 0.01024409), (-0.07279013, 0.06439988, 0.01520595), (-0.07280136, 0.06438259, 0.01208908)]



solution = op.minimize(objective,np.array([1,1,1,1]),points)

#print(solution)
print(solution.x)
print(solution.fun)
print(perp_error(solution.x,points))

#op.minimize(perp_error())
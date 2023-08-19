import numpy as np
from math import sqrt, atanh, sinh, cosh

"""
This script includes a variety of functions and classes written for the development of a simple game showcasing the 
effects of special relativity.

The functions written are simplified under the assumption that relativistic effects are only appreciable in the 
x direction. Relativistic effects from motion along other dimensions are ignored

Doppler shift and its impact on the display are also ignored (for the moment), however these effects can be seen 
in an MIT student project called A Slower Speed of Light
"""

C = 299_792_458  # meters/second speed of light in reality


def minkowski_magnitude(four_vector) -> float:
    minkowski_metrix_tensor = np.diag([1, -1, -1, -1])
    temp = np.matmul(minkowski_metrix_tensor, four_vector)
    return np.matmul(four_vector.T, temp).item()


def calc_four_velocity(vx=0, c=C):
    # Minkowski Metric |U|^2 = 0 = (ct)^2 -vx^2 -vy^2 -vz^2
    # (ct)^2 = vx^2 +vy^2 +vz^2
    gamma, beta = lorentz_factor(vx=0, c=c)
    dct_dctau = gamma
    dx_dctau = gamma*vx
    return dct_dctau, dx_dctau


def calc_four_acceleration(a, u, c):
    pass


def lorentz_factor(vx, c=C):
    # Gamma = 1/sqrt(1-v^2/c^2)
    beta_coeff = vx/c  # Percentage of the speed of light
    radicand = 1 - beta_coeff**2
    gamma = radicand**(-1/2)
    return gamma, beta_coeff


def lorentz_transform(vx, ct, x, y, c=C):
    if abs(vx) >= C:
        raise ValueError(f'Speed: {vx} greater than the speed of light used: {c}')
    gamma, beta = lorentz_factor(vx, c=C)
    new_ct = gamma*(ct - beta*x)
    new_x = gamma*(-beta*ct+x)
    return new_ct, new_x, y


def rindler_transform(vx, ax, ct, x, y, c=C):
    d = c**2/ax  # Distance to rindler horizon
    new_ct = x*sinh(ct/d)
    new_x = x*cosh(ct/d)
    return new_ct, new_x, y


def calc_rapidity(v, c) -> float:
    return atanh(v/c)


def inverse_rindler_transform(ax, ct, x, y, c=C):
    # Inverse Rindler Transformation
    new_ct = c**2/ax*atanh(ct/x)
    new_x = sqrt(x**2 - ct**2)
    return new_ct, new_x, y


if __name__ == '__main__':
    test_vel = np.array([[0, 0, 0, 298000000]]).T
    print(lorentz_transform(vx=test_vel, ct=1, x=1, y=1))

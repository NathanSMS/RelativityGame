import numpy as np
from math import sqrt, atanh

"""
This script includes a variety of functions and classes written for the development of a simple game showcasing the 
effects of special relativity.

The functions written are simplified under the assumption that relativistic effects are only appreciable in the 
x direction. Relativistic effects from motion along other dimensions are ignored

Doppler shift and its impact on the display are also ignored (for the moment), however these effects can be seen 
in an MIT student project called A Slower Speed of Light
"""

C = 299_792_458  # meters/second speed of light in reality


def lorentz_factor(v, c=C):
    # Gamma = 1/sqrt(1-v^2/c^2)
    beta_coeff = v/c  # Percentage of the speed of light
    radicand = 1 - beta_coeff**2
    gamma = radicand**(-1/2)
    return gamma, beta_coeff

def lorentz_transform(frame_velocity, four_vec, c=C):
    # Returns the lorentz transform matrix from the current frame (taken as stationary) into the desired (moving) frame
    # The given velocity is the velocity of the desired frame as measured in the current frame

    transform = np.eye(4)  # Start w/ 4D identity and successively multiply through 3 lorentz boosts, one per axis
    for dim in range(1, 4):

        v = frame_velocity[dim, 0]

        gamma, beta = lorentz_factor(v, c)
        inter_transformation = np.eye(4)
        inter_transformation[0, 0] = gamma
        inter_transformation[0, dim] = -gamma*beta
        inter_transformation[dim, 0] = -gamma*beta
        inter_transformation[dim, dim] = gamma

        transform = np.matmul(transform, inter_transformation)
    print(transform)

    return np.matmul(transform, four_vec)


def rindler_transform(frame_velocity, frame_acceleration, four_vec, c=C):
    # Currently only

    ...


def inverse_rindler_transform(position, alpha, c=C):
    # Inverse Rindler Transformation
    ct = c**2/alpha*atanh(position.ct/position.x)
    x = sqrt(position.x**2 - position.ct**2)
    y = position.y
    z = position.z
    return np.array([[ct, x, y, z]]).T


if __name__ == '__main__':
    test_vel = np.array([[0, 0, 0, 298000000]]).T
    print(lorentz_transform(frame_velocity=test_vel, four_vec=np.ones(shape=(4, 1), dtype=float)))

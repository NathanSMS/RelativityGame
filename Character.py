from PhysicsObject import PhysicsObject
import SpecialRelativity as SR
import pygame
import numpy as np


class Character(PhysicsObject):
    def __init__(self):
        super(PhysicsObject, self).__init__(self, ct=0, x=0, vx=0, ax=0, mass=1)

    def jump(self):
        if self.isGrounded:
            self.vy = 50
            self.isGrounded = False


if __name__ == '__main__':
    pygame.init()
    pass
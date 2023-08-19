import math

import pygame
import SpecialRelativity as SR
import numpy as np
from collections import namedtuple
from math import sin

pygame.init()
vec = namedtuple('vector','ct x y')

class Camera:

    def __init__(self, resolution: tuple = (1000, 800), fps: int = 60, name: str = 'Super Lorentz Bros', t=0, x=0, y=None, vx=0, ax=0):
        # Resolution passed as tuple (width, height)
        self.fps = fps
        self.window = pygame.display.set_mode(resolution, flags=pygame.SCALED)
        pygame.display.set_caption(name)
        self.background_img = 'Assets/planet_background.jpg'
        self.clock = pygame.time.Clock()
        self.t = t
        self.x = x
        if y is None:
            y = resolution[1]
        self.y = y
        self.vx = vx
        self.ax = ax

    def time_step(self):
        # Game display is done wrt camera object, frame rate should be (relatively) constant in this frame
        # calling the time_step() method returns the interval of time passed since the last frame WRT the level frame
        gamma, beta = SR.lorentz_factor(self.vx)
        dt_cam = self.clock.tick(60)/1000  # Convert ms to s
        self.t += dt_cam
        return dt_cam*gamma

# ATM THIS JUST WORKS LIKE BLIT, NEED TO ADD CODE TO MAKE IT WORK HOW I WANT
    def draw_to_screen(self, items=None):
        # Pass in items as list of objects with surface and position attributes

        if items is None:
            return
        else:
            for item in items:
                transformed_surface, transformed_pos = self.transform_surface(item)

                self.window.blit(transformed_surface, transformed_pos)

        pygame.display.update()

    def clear_screen(self):
        bg_surface = pygame.image.load(self.background_img)
        self.window.blit(bg_surface, (0, 0))

    @staticmethod
    def update():
        pygame.display.update()

    def transform_surface(self, phys_object, c=SR.C):

        # Get necessary info and do 'regular' transformation prior to relativistic adjustments
        x = phys_object.x - self.x  # Shift along x so level & cam coordinates share origin
        y = self.y - phys_object.y  # Shift and flip along y
        proper_width = phys_object.proper_width
        proper_height = phys_object.proper_height
        screen_height = self.window.get_height()
        surface = phys_object.surface

        # Check if accelerating or not for lorentz vs rindler transformation
        if self.ax == 0.0:  # if A = zero vector do lorentz transform
            gamma, beta = SR.lorentz_factor(self.vx)  # Get important SR factors
            new_x = gamma * (x - beta * self.t * c)  # Adjust x coord
            new_y = y  # Adjust y coord to camera frame
            new_width = gamma * proper_width
            new_size = (new_width, proper_height)

            transformed_surface = pygame.transform.smoothscale(surface, new_size)
            transformed_pos = (new_x, new_y)

            print(f'Level Frame  X: {phys_object.x} Y: {phys_object.y}')
            print(f'Camera Frame X: {new_x} Y: {new_y}')
            print('---------------------')

            return transformed_surface, transformed_pos
        else:
            # do rindler transformation
            #return SR.rindler_transform(yadayadayada)
            raise NotImplementedError


if __name__ == '__main__':
    ABS_PATH = '/home/nathan/PycharmProjects/RelativityGame/Assets/Individual Sprites/'

    pygame.init()
    
    RESOLUTION = (800, 400)
    WIDTH = 100
    HEIGHT = 200
    # test_surface = pygame.image.load('Assets/Individual Sprites/adventurer-idle-00.png')
    # test_surface.fill('Red')

    cam = Camera(resolution=RESOLUTION, x=0, y=0, vx=0)

    surf1 = pygame.image.load(ABS_PATH+'adventurer-idle-00.png').convert_alpha()
    surf2 = pygame.image.load(ABS_PATH+'adventurer-attack2-00.png').convert_alpha()

    Item = namedtuple('Item','surface x y proper_width proper_height')

    item1 = Item(surf1, 100, 200, 50, 50)
    item2 = Item(surf2, 200, 250, 50, 50)

    tau = 0  # Level time
    while True:
        dtau = cam.time_step()
        tau += dtau
        cam.vx = SR.C*0.9999*math.sin(tau)
        print(f'Level Time: {tau:.2f}, Camera Time: {cam.ct:.2f}, Camera Velocity: {cam.vx/SR.C:.2f}c')
        cam.clear_screen()
        cam.draw_to_screen([item1, item2])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Redundant here I believe
                pygame.quit()
                exit()
        cam.update()

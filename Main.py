import pygame
import Camera
from sys import exit
import os
import random
import numpy as np

import Character
import PhysicsObject
from os import listdir
from os.path import isfile,join


###
# Initialize window, game, load in assets
###

if __name__ == '__main__':
    pygame.init()

    BACKGROUND_COLOR = (255, 255, 255)  # RGB TEMP
    PLAYER_VEL = 5  # TEMP, to be replaced w/ OOP stuff
    C = 30

    cam = Camera.Camera()
    dynamic_objects = set([])
    static_objects = set([])

    player = Character.Character()
    dynamic_objects.add(player)

    FORCE_STRENGTH = 10  # How quickly the player accelerates

    running = True
    while running:
        d_tau = cam.time_step()  # Get level time pass from camera's frame

        ###
        # Process Inputs
        ###
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Redundant here I believe
                pygame.quit()
                exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.jump()
            if keys[pygame.K_s]:
                ...  # player.crouch()?
            if keys[pygame.K_a]:
                player.apply_force(-FORCE_STRENGTH)
            if keys[pygame.K_d]:
                player.apply_force(FORCE_STRENGTH)

        #
        # Do kinematics in World Frame
        #
        for obj in dynamic_objects:
            obj.time_step(d_tau)

        #
        # Process any collisions
        #

        #
        # Perform relativistic Shifts to Camera Coord system
        #

        #
        # Display Objects & Stuffs
        #

        all_drawn_items = dynamic_objects.union(static_objects)
        cam.draw_to_screen(all_drawn_items)

pygame.quit()
quit()

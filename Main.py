import pygame
from Camera import Camera
from sys import exit
import os
import random
import numpy as np
from PhysicsObject import PhysicsObject
from os import listdir
from os.path import isfile,join

do_Display = True

if __name__ == '__main__':
    pygame.init()
    tau = 0  # Level Time
    RES = (1800, 1000)
    cam = Camera(resolution=RES, t=tau, y=RES[1])  # Start camera location off at (0, screen height)

    # Create a font for game info
    game_font = pygame.font.Font(None, 50)
    score = 0

    # TEMP
    player = PhysicsObject(x=200, y=800)
    ground = PhysicsObject(x=0, y=100, width=1800, height=100, is_dynamic=False, img=None)

    while True:
        cam.clear_screen()

        # Keep track of level time
        d_tau = cam.time_step()  # this gives a time-dilation adjusted time step according to the camera speed
        tau += d_tau  # PhysicsObject should keep track of level time as well, but Ill leave this for now
        PhysicsObject.apply_time_step(dtau=d_tau)  # Update kinematics for all physics objects

        # Display Stuff
        if do_Display:
            bg_text = pygame.Surface((300, 140))
            bg_text.fill('Black')
            cam.window.blit(bg_text, (0, 0))
            level_time_surface = game_font.render(f'Level Time:   {tau:.2f}', False, 'White')
            cam.window.blit(level_time_surface, (10, 10))
            player_time_surface = game_font.render(f'Player Time: {player.t:.2f}', False, 'White')
            cam.window.blit(player_time_surface, (10, 50))
            score_surface = game_font.render(f'Score: {score}', False, 'White')
            cam.window.blit(score_surface, (10, 90))
            cam.draw_to_screen(PhysicsObject.get_all_objects())
        else:  # AI Learning To Play, Display Not Necessary
            ...

        # Process Inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Redundant here I believe
                pygame.quit()
                exit()

        pygame.display.update()

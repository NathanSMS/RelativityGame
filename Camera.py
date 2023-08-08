import pygame
import SpecialRelativity as SR
import numpy as np

pygame.init()


column_vec = (4, 1)
vec_type = float

class Camera:

    def __init__(self, resolution: tuple = (1000, 800), fps: int = 60, name: str = 'Super Lorentz Bros', four_pos=np.zeros(shape=column_vec, dtype=vec_type), four_vel=np.zeros(shape=column_vec, dtype=vec_type), four_acc=np.zeros(shape=column_vec, dtype=vec_type)):
        # Resolution passed as tuple (width, height)
        self.fps = fps
        self.window = pygame.display.set_mode(resolution, flags=pygame.SCALED)
        pygame.display.set_caption(name)
        self.clock = pygame.time.Clock()
        self.four_pos = four_pos
        self.four_vel = four_vel
        self.four_acc = four_acc

    def time_step(self):
        # Game display is done wrt camera object, frame rate should be (relatively) constant in this frame
        # calling the time_step() method returns the interval of time passed since the last frame WRT the level frame

        gamma, beta = SR.lorentz_factor(v=self.four_vel[1])
        dt_cam = self.clock.tick(60)
        self.four_pos += self.four_vel*dt_cam
        self.four_vel += self.four_acc*dt_cam
        # self.four_acc  # tbd

        d_tau = gamma*dt_cam - gamma*beta*float(self.four_pos[1])  # Perform lorentz transformation for just x velocity for cam
        d_tau = float(d_tau)
        print(f'dtau is type: {type(d_tau)}')
        return d_tau

# ATM THIS JUST WORKS LIKE BLIT, NEED TO ADD CODE TO MAKE IT WORK HOW I WANT
    def draw_to_screen(self, items=None):
        # Pass in items as (surface, position_in_level)

        if items is None:
            return
        else:
            for item in items:
                # transform each item's level coordinates to the camera coordinates

                item_surface = item[0]
                item_level_4pos = np.array([[0, item[1][0], item[1][1], 0]]).T


                # calculate new position and size in camera frame
                transformed_4pos = self.get_transformed(item_level_4pos)

                new_x = int(transformed_4pos[1].item())
                new_y = int(transformed_4pos[2].item())

                transformed_position = (new_x, new_y)  # CHANGE THIS TO CALCULATIONS
                print(f'transformed position: {transformed_position}')

                width = item_surface.get_width()
                height = item_surface.get_height()
                temp_array = np.array([[0, width, height, 0]]).T
                temp_transformed = self.get_transformed(temp_array)
                new_width = int(temp_transformed[1].item())
                new_height = int(temp_transformed[2].item())

                # transform items personal surface to fit dimensions in camera coordinates
                transformed_surface = pygame.transform.smoothscale(item_surface, (new_width, new_height))

                # blit transformed surface
                self.window.blit(transformed_surface, transformed_position)

        pygame.display.update()

    def get_transformed(self, four_vec):
        transform_matrix = np.eye(4)

        if np.linalg.norm(self.four_acc, ord=2) == 0.0:  # if A = zero vector
            # Check if Four Acceleration is null vector
            # Do lorentz transformation
            new_vec = SR.lorentz_transform(self.four_vel, four_vec)

            # Camera coordinates flip y and start from top of screen
            new_vec[2] = self.window.get_height() - new_vec[2]
            return new_vec
        else:
            # do rindler transformation
            #return SR.rindler_transform(yadayadayada)
            raise NotImplementedError


if __name__ == '__main__':
    pygame.init()
    
    RESOLUTION = (800, 400)
    WIDTH = 100
    HEIGHT = 200
    # test_surface = pygame.image.load('Assets/Individual Sprites/adventurer-idle-00.png')
    # test_surface.fill('Red')

    cam = Camera(resolution=RESOLUTION, four_vel=np.array([[0, 0.1*SR.C, 0, 0]]).T)

    surf1 = pygame.image.load('Assets/Individual Sprites/adventurer-die-00.png').convert_alpha()
    surf2 = pygame.image.load('Assets/Individual Sprites/adventurer-attack2-00.png').convert_alpha()

    item1 = (surf1, (0, 350))
    item2 = (surf2, (200, 100))

    cam.draw_to_screen([item1, item2])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Redundant here I believe
                pygame.quit()
                exit()
        cam.clock.tick(60)

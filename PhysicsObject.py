import SpecialRelativity as SR
import numpy as np
import pygame

G = 9.81  # m/s/s regular gravitational acceleration

class PhysicsObject:

    def __init__(self, four_pos=None, four_vel=None, four_acc=None, mass=1):
        if four_pos is None:
            self.FourPos = np.zeros(shape=(4, 1), dtype=float)
        elif four_vel is None:
            self.FourVel = np.array([1, 0, 0, 0], shape=(4, 1), dtype=float)
        elif four_acc is None:
            self.FourAcc = np.zeros(shape=(4, 1), dtype=float)
        self.mass = mass
        self.isGrounded = True
        self.animationCount = 0
        # self.sprite =

    def apply_force(self, force):
        # Force given as 4x1 numpy array
        gamma, beta = SR.lorentz_factor(v=self.FourVel[2])

        four_force = np.array([[-gamma*beta*force, gamma*force, -G*self.mass, 0]]).T

        self.FourAcc = four_force/self.mass

    def time_step(self, d_tau):
        # Takes in length of proper time step to use for numerical integration
        if self.isGrounded:
            # self.FourAcc[2] = 0
            self.FourVel[2] = 0

        self.FourPos += self.FourVel*d_tau
        self.FourVel += self.FourAcc*d_tau
        self.FourAcc = np.array([[0, 0, -G, 0]]).T

        self.animationCount += 1

    def draw(self, window):
        screen_pos = pygame.Vector2(self.FourPos.x, window.get_height() - self.FourPos.y)
        pygame.draw.circle(window, 'red', screen_pos, 40)


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0.01

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        pygame.draw.circle(screen, "red", player_pos, 40)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for frame rate
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

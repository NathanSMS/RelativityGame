from PhysicsObject import PhysicsObject
import SpecialRelativity as SR
import pygame
import numpy as np

class Character(PhysicsObject):
    def __init__(self):
        super(PhysicsObject, self).__init__(self, four_pos=None, four_vel=None, four_acc=None, mass=1)
        self.state = 'idle'
        self.animationCount = 0

    def draw(self, screen):
        x = self.FourPos.x
        y = self.FourPos.y
        pygame.draw.circle(screen, "red", (x,y), 40)

    def jump(self):
        if self.isGrounded:
            self.FourVel.y += 20
            self.isGrounded = False
        ...

player = Character()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dTau = 0.01

    player.FourPos.x = screen.get_width() / 2
    player.FourPos.y = screen.get_height() / 2

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dTau = player.get_dTau()


        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")



        player.draw(screen)

        

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dTau = clock.tick(60) / 1000

    pygame.quit()
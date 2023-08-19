import SpecialRelativity as SR
import numpy as np
import pygame

g = 9.81  # m/s/s regular gravitational acceleration


class PhysicsObject:
    C = 299_792_458  # m/s speed of light
    g = 9.81  # m/s/s earth surface gravity
    dynamic_objects = []
    static_objects = []
    tau = 0  # Proper time for level reference frame, all other coords measured w/ respect to this level reference frame

    def __init__(self, t=0, x=0, y=0, dt=1, vx=0, vy=0, ax=0, ay=-1000, mass=1, width=100, height=100,
                 img='Assets/Individual Sprites/adventurer-idle-00.png', is_dynamic=True):
        # All values (unless specified otherwise) are measured within the level frame
        self.t = t
        self.x = x
        self.y = y
        self.dt = dt
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.mass = mass
        self.isGrounded = True
        self.state = 'idle'
        self.animationCount = 0
        self.proper_width = width  # Object width in its rest frame
        self.proper_height = height  # Object height in its rest frame
        self.img = img
        self.is_dynamic = is_dynamic

        if img is not None:
            self.surface = pygame.image.load(self.img)
        else:
            self.surface = pygame.surface.Surface((width, height))
            self.surface.fill('Green')

        self.add_to_objects(self, obj_is_dynamic=is_dynamic)

    @classmethod
    def static_object(cls, x=0, y=0, width=50, height=50, img=None):
        return cls.__init__(x=x, y=y, vx=0, vy=0, ax=0, ay=0, width=width, height=height, is_dynamic=False, img=None)

    @classmethod
    def from_image(cls, image_path):
        surf = pygame.image.load(image_path)
        width, height = surf.get_size()
        return PhysicsObject(width=width, height=height)

    @classmethod
    def add_to_objects(cls, obj, obj_is_dynamic):
        if obj not in cls.dynamic_objects and obj_is_dynamic:
            cls.dynamic_objects.append(obj)
        elif obj not in cls.static_objects and not obj_is_dynamic:
            cls.static_objects.append(obj)

    @classmethod
    def remove_from_objects(cls, obj):
        if obj in cls.dynamic_objects:
            cls.dynamic_objects.remove(obj)
        elif obj in cls.static_objects:
            cls.static_objects.remove(obj)

    @classmethod
    def apply_time_step(cls, dtau=0.01):
        # Applies the timestep to all physics objects, processes collisions, etc.
        for obj in cls.get_all_objects():
            if obj.is_dynamic:
                obj.time_step(dtau=dtau)
        cls.tau += dtau

    @classmethod
    def get_all_objects(cls):
        return cls.dynamic_objects + cls.static_objects

    def __str__(self):
        return f'Level Time: {self.tau:.2f}, ct: {self.t:.2f}, x: {self.x:.2f}, y: {self.y:.2f}'

    def apply_force(self, force):
        fx, fy = force
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def time_step(self, dtau):
        gamma, _ = SR.lorentz_factor(self.vx)
        self.t += gamma * dtau
        self.x += self.vx * gamma * dtau
        self.y += self.vy * gamma * dtau
        self.vx += self.ax * dtau
        self.vy += self.ay * dtau
        # self.ax = 0
        # self.ay = 0

    def draw(self, window):
        rectangle = pygame.Rect(self.x, window.get_height() - self.y, self.proper_width, self.proper_height)
        pygame.draw.rect(window, 'red', rectangle, width=0)

    def check_collision(self, other):
        pass


if __name__ == '__main__':
    # Initialize Game Stuff
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    t_start = 0
    x_start = screen.get_width() / 2
    y_start = screen.get_height() / 2

    test_obj = PhysicsObject(t=t_start, x=x_start, y=y_start, vx=0.95 * SR.C, vy=500)
    test_obj2 = PhysicsObject(t=t_start, x=x_start / 2, y=y_start / 2, vx=-200, vy=-150)

    while running:
        dtau = clock.tick(60) / 1000  # limits FPS to 60, get time since last frame in seconds
        # dtau is delta time in seconds since last frame, used for frame rate
        # independent physics.
        print(str(test_obj))
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("Black")

        PhysicsObject.apply_time_step(dtau=dtau)

        for object in [test_obj, test_obj2]:
            radius = 35
            elasticity = 0.75
            if object.y - radius <= 0:
                object.y = radius
                object.vy *= -elasticity
            if object.x <= radius:
                object.x = radius
                object.vx *= -elasticity
            elif object.x >= screen.get_width() - radius:
                object.x = screen.get_width() - radius
                object.vx *= -elasticity

            object.draw(screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            pass
        if keys[pygame.K_s]:
            pass
        if keys[pygame.K_a]:
            pass
        if keys[pygame.K_d]:
            pass

        # flip() the display to put your work on screen
        pygame.display.flip()
    pygame.quit()

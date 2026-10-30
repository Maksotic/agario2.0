import pygame
from dataclasses import dataclass, field
import random
import math

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
window = pygame.display.set_mode((400, 400))
scalefactor = 1
@dataclass
class Player:
    x:int = 200
    y:int = 200
    radius:int = 20
    color:tuple = (0, 0, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def get_hitbox(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def check_collision(self, food_object):
        fh = food_object.get_hitbox()
        ph = self.get_hitbox()

        if fh.colliderect(ph):
            return True

        return False
@dataclass
class Food:
    color:tuple = RED
    x:int = field(default_factory=lambda: random.randint(0, 800))
    y:int = field(default_factory=lambda: random.randint(0, 800))
    eaten:bool = False
    radius:int = 20
    def draw(self, screen):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius/scalefactor)

    def get_hitbox(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.y += 10
        if keys[pygame.K_DOWN]:
            self.y -= 10
        if keys[pygame.K_LEFT]:
            self.x += 10
        if keys[pygame.K_RIGHT]:
            self.x -= 10


food = list()
food_eaten = 0

player = Player()


for i in range(200):
    f = Food()
    food.append(f)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(WHITE)
    #draw
    for x in food:
        if x.eaten == False:
            x.draw(window)
            x.update()

            if player.check_collision(x):
                x.eaten = True
                scalefactor = math.exp(0.08 * food_eaten)
                if scalefactor >= 3:
                    scalefactor = 2
                food_eaten += 1
    player.draw(window)


    clock.tick(60)
    pygame.display.flip()

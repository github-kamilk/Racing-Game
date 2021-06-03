import pygame
from pygame.locals import *
import random

pygame.init()

FPS = 30
framesPerSec = pygame.time.Clock()

black = (0, 0, 0)

window = pygame.display.set_mode((550, 750))
window.fill(black)
pygame.display.set_caption("Kart")

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/block.png")
        self.surface = pygame.Surface((256, 40))
        self.rect = self.surface.get_rect(center=(random.randint(100, 1000), 0))

    def move(self):
        self.rect.move_ip(0,10)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.center = (random.randint(100,1000),0)

    def draw(self, surface):
        surface.blit(self.image,self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("data/ferrari.png")
        self.surface = pygame.Surface((115, 240))
        self.rect = self.surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-300))

    def draw(self, surface):
        surface.blit(self.image,self.rect)

    def update(self):
        pressedKeys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressedKeys[K_LEFT]:
                self.rect.move_ip(-5,0)

        if self.rect.right < SCREEN_WIDTH:
            if pressedKeys[K_RIGHT]:
                self.rect.move_ip(5,0)

P1 = Player()
O1 = Obstacle()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    P1.update()
    O1.move()

    window.fill(black)

    P1.draw(window)
    O1.draw(window)

    pygame.display.update()
    framesPerSec.tick(FPS)

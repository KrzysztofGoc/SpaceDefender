from pygame.sprite import Sprite
import pygame
from random import randint

class Planet(Sprite):
    def __init__(self, image_number, screen, planets):
        super(Planet, self).__init__()
        if image_number == 0:
            self.image = pygame.image.load('images/big_planet.gif')
            self.rect = self.image.get_rect()
        elif image_number == 1:
            self.image = pygame.image.load('images/small_red_planet.gif')
            self.rect = self.image.get_rect()
        elif image_number == 2:
            self.image = pygame.image.load('images/small_grey_planet.gif')
            self.rect = self.image.get_rect()
        elif image_number == 3:
            self.image = pygame.image.load('images/small_green_planet.gif')
            self.rect = self.image.get_rect()
        elif image_number == 4:
            self.image = pygame.image.load('images/small_destroyed_planet.gif')
            self.rect = self.image.get_rect()
        elif image_number == 5:
            self.image = pygame.image.load('images/small_crushed_planet.gif')
            self.rect = self.image.get_rect()
        self.screen = screen.get_rect()
        self.rect.x = randint(60, self.screen.width - 60)
        self.rect.y = randint(60, self.screen.height - 60)
        if planets:
            for planet in planets:
                if planet.rect.x - self.rect.x < 30:
                    self.rect.x += 100
                elif planet.rect.y - self.rect.y < 70:
                    self.rect.y += 100

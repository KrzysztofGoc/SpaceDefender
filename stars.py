from pygame.sprite import Sprite
import pygame
from random import randint


class Star(Sprite):
    def __init__(self, image_number, screen):
        super(Star, self).__init__()
        if image_number == 0:
            self.image = pygame.image.load('images/star1.png')
        elif image_number == 1:
            self.image = pygame.image.load('images/star2.png')
        elif image_number == 2:
            self.image = pygame.image.load('images/star3.png')
        self.rect = self.image.get_rect()
        self.screen = screen.get_rect()
        self.rect.x = randint(0, self.screen.width)
        self.rect.y = randint(0, self.screen.height)

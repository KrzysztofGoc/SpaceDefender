import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from health import Health


class Alien(Sprite):
    def __init__(self, screen, ai_settings):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/basic_alien.gif')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.health = 1
        self.alien_health_bars = Group()

    def update_alien_lives(self):
        for live in range(self.health):
            alien_health = Health(self.rect, self.ai_settings, self.alien_health_bars, self.health, self.screen)
            self.alien_health_bars.add(alien_health)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x


class BetterAlien(Alien):
    def __init__(self, screen, ai_settings):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/better_alien.gif')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.health = 2
        self.alien_health_bars = Group()
        self.speed = 1


class SuperAlien(Alien):
    def __init__(self, screen, ai_settings):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/super_alien.gif')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.health = 3
        self.alien_health_bars = Group()
        self.speed = 0.75

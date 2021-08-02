import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship, stats):
        super(Bullet, self).__init__()
        self.stats = stats
        self.screen = screen
        self.image = pygame.image.load('images/basic_bullet.gif')
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        if self.stats.level == 3:
            self.x += 15
            self.rect.x = self.x
        else:
            self.y -= self.speed_factor
            self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
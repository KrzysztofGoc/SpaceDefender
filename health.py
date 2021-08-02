import pygame
from pygame.sprite import Sprite

class Health(Sprite):
    def __init__(self, alien_rect, ai_settings, alien_health_bars, health, screen):
        super(Health, self).__init__()
        self.health = health
        self.ai_settings = ai_settings
        self.color = self.ai_settings.health_color
        self.screen = screen
        self.width = alien_rect.width
        if health > 1:
            self.rect = pygame.Rect(0, 0, self.width / self.health, 3)
        elif health == 1:
            self.rect= pygame.Rect(0, 0, self.width / 2, 3)
        self.rect.top = alien_rect.bottom + 10
        if health != 1:
            self.rect.x = alien_rect.left - 3 + (len(alien_health_bars) * (self.rect.width + 5))
        elif health == 1:
            self.rect.x = alien_rect.centerx - 17

    def draw_alien_lives(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

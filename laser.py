from pygame.sprite import Sprite
import pygame


class Laser(Sprite):
    def __init__(self, stats):
        super(Laser, self).__init__()
        self.stats = stats
        self.image = pygame.image.load('images/laser.gif')
        self.rect = self.image.get_rect()
        self.rect.left = 235
        self.rect.y = 875
        self.laser_y = float(self.rect.y)

    def check_laser_height(self):
        if self.stats.level == 3:
            if self.rect.top <= 723:
                return True

    def update(self):
        if self.check_laser_height():
            self.set_laser()
        else:
            self.laser_y -= 0.25
            self.rect.y = self.laser_y

    def set_laser(self):
        if self.stats.level == 3:
            self.rect.y = 875
            self.laser_y = 875

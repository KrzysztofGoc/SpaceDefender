import pygame.font
from ship import Ship
from alien import SuperAlien
from bullet import Bullet
from ship import ShipLives
from alien import Alien
from laser import Laser
from time import sleep


class Button():
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (158, 0, 93)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('images/font/ca.ttf', 48)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Bonuses(Button):
    def __init__(self, ai_settings, screen, msg, msg2, msg3, bullets, aliens, stats, shiplives, aliens_bonus, lasers):
        super().__init__(ai_settings, screen, msg)
        self.lasers = lasers
        self.aliens_bonus = aliens_bonus
        self.shiplives = shiplives
        self.stats = stats
        self.aliens = aliens
        self.bullets = bullets
        self.ai_settings = ai_settings
        self.rect.center = self.screen_rect.center
        self.font = pygame.font.Font('images/font/ca.ttf', 32)
        self.text_color = (255, 255, 255)
        self.button_color = (27, 20, 100)
        self.image = pygame.image.load('images/menu.gif')
        self.rect = self.image.get_rect()
        self.ship_speed = 0.5
        self.ship_direction = 1
        self.prepare_bonuses_background()
        self.prep_first_msg(msg)
        self.prep_second_msg(msg2)
        self.prep_third_msg(msg3)

    def prepare_bonuses_background(self):
        self.background_image = pygame.image.load('images/bonuses_background.gif')
        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = self.screen_rect.center

    def update_first_bonus(self):
        self.check_ship_height()
        self.y += self.ship_speed * self.ship_direction
        self.ship.rect.y = self.y

    def check_ship_height(self):
        if self.ship.rect.y == 200 and not self.aliens:
            new_alien = SuperAlien(self.screen, self.ai_settings)
            new_alien.rect.y = 240
            new_alien.rect.x = self.ship.rect.x + 350
            new_alien.health = 6
            new_alien.update_alien_lives()
            self.aliens.add(new_alien)
        if self.ship.rect.y + self.ship.rect.height == 350 or self.ship.rect.y == 190:
            if self.ship.rect.y + self.ship.rect.height == 350 and not self.bullets:
                new_bullet = Bullet(self.ai_settings, self.screen, self.ship, self.stats)
                new_bullet.image = pygame.image.load('images/basic_bullet_side.gif')
                new_bullet.rect.y = self.ship.rect.centery
                new_bullet.rect.x = self.ship.rect.left
                self.bullets.add(new_bullet)
            self.ship_direction = self.ship_direction * -1

    def prep_first_msg(self, msg1):
        self.msg_font1 = self.font.render(msg1, True, self.text_color, self.button_color)
        self.msg_font1_rect = self.msg_font1.get_rect()
        self.msg_font1_rect.left = self.background_rect.left + 125
        self.msg_font1_rect.top = self.background_rect.top + 80

        self.ship = Ship(self.ai_settings, self.screen)
        self.ship.image = pygame.image.load('images/ship_live_side.gif')
        self.ship.rect = self.ship.image.get_rect()
        self.ship.rect.x = self.msg_font1_rect.left
        self.ship.rect.y = 200
        self.y = float(self.ship.rect.y)

    def prep_second_msg(self, msg2):
        self.msg_font2 = self.font.render(msg2, True, self.text_color, self.button_color)
        self.msg_font2_rect = self.msg_font2.get_rect()
        self.msg_font2_rect.left = self.background_rect.left + 125
        self.msg_font2_rect.top = self.msg_font1_rect.bottom + 250
        self.add_lives(4)

    def add_lives(self, number):
        for _ in range(number):
            new_live = ShipLives(self.screen, self.ai_settings)
            new_live.rect.y = self.msg_font2_rect.bottom + 30
            new_live.rect.x = self.msg_font2_rect.left + len(self.shiplives) * 60
            self.shiplives.add(new_live)

    def prep_third_msg(self, msg3):
        self.msg_font3 = self.font.render(msg3, True, self.text_color, self.button_color)
        self.msg_font3_rect = self.msg_font3.get_rect()
        self.msg_font3_rect.left = self.background_rect.left + 125
        self.msg_font3_rect.top = self.msg_font2_rect.bottom + 250
        self.x = float(self.msg_font3_rect.x)
        self.add_aliens()
        self.add_laser()

    def add_laser(self):
        self.laser = Laser(self.stats)
        self.lasers.add(self.laser)

    def add_aliens(self):
        for _ in range(17):
            new_alien = Alien(self.screen, self.ai_settings)
            new_alien.image = pygame.image.load('images/small_alien.gif')
            new_alien.rect.y = self.msg_font3_rect.bottom + 90
            new_alien.rect.x = self.msg_font3_rect.left + (len(self.aliens_bonus) * 60)
            self.aliens_bonus.add(new_alien)

    def draw_bonuses(self):
        self.screen.blit(self.background_image, self.background_rect)
        self.screen.blit(self.msg_font1, self.msg_font1_rect)
        self.screen.blit(self.msg_font2, self.msg_font2_rect)
        self.screen.blit(self.msg_font3, self.msg_font3_rect)
        self.ship.blitme()

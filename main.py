import pygame
from settings import Ustawienia
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from game_functions import random_planets
from game_functions import random_stars
from button import Bonuses


def run_game():
    pygame.init()
    screen = pygame.display.set_mode(size=(0, 0), flags=pygame.FULLSCREEN)
    ai_settings = Ustawienia(screen)
    pygame.display.set_caption("Inwazja obcych")
    play_button = Button(ai_settings, screen, "Gra")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    lasers = Group()
    true_lasers = Group()
    bullets = Group()
    aliens = Group()
    aliens_bonus = Group()
    shiplives = Group()
    shiplives_bonus = Group()
    planets = Group()
    stars = Group()
    random_planets(planets, screen)
    random_stars(stars, screen)
    bonuses1 = Bonuses(ai_settings, screen, "Upgraded bullets - your bullets now hit for 2 health points",
                       "Full your healthbar + add 4th life", "Click X to destroy all aliens on the screen",
                       bullets, aliens, stats, shiplives_bonus, aliens_bonus, lasers)
    gf.create_fleet(ai_settings, screen, ship, aliens, stats)

    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, shiplives, bonuses1,
                        true_lasers)
        if stats.game_active is False and stats.bonuses_shown is True:
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, true_lasers)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, true_lasers)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, shiplives)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, shiplives, planets,
                         stars, bonuses1, shiplives_bonus, aliens_bonus, lasers, true_lasers)


if __name__ == '__main__':
    run_game()

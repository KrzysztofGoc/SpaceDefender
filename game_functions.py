import sys
import pygame
from bullet import Bullet
from alien import Alien
from alien import BetterAlien
from alien import SuperAlien
from time import sleep
from ship import ShipLives
import json
from random import randint
from planet import Planet
from stars import Star
from threading import Thread
from laser import Laser


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, true_lasers):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets, stats)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        if stats.score >= stats.high_score:
            with open('score.json', 'w') as wynik:
                json.dump(stats.high_score, wynik)
        sys.exit()
    elif event.key == pygame.K_p:
        aliens.empty()
    elif event.key == pygame.K_x and stats.can_use_laser:
        use_laser(true_lasers, stats)


def use_laser(true_lasers, stats):
    new_laser = Laser(stats)
    new_laser.image = pygame.image.load('images/laserr.gif')
    new_laser.rect = new_laser.image.get_rect()
    new_laser.rect.left = 0
    new_laser.rect.y = 980
    true_lasers.add(new_laser)


def random_stars(stars, screen):
    for _ in range(randint(60, 100)):
        image_number = randint(0, 2)
        star = Star(image_number, screen)
        stars.add(star)
    for star in stars:
        for stara in stars:
            if star.rect.x == stara.rect.x:
                star.rect.x += 15


def random_planets(planets, screen):
    for _ in range(randint(3, 8)):
        image_number = randint(0, 5)
        planet = Planet(image_number, screen, planets)
        planets.add(planet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb, shiplives):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        button_start_on_click(ai_settings, stats, aliens, bullets, ship, screen, shiplives, sb)


def button_start_on_click(ai_settings, stats, aliens, bullets, ship, screen, shiplives, sb):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens, stats)
    ship.center_ship()
    sb.prep_texts()
    update_lives(screen, ai_settings, shiplives, stats)


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb, shiplives, bonuses1, lasers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if stats.score >= stats.high_score:
                with open('score.json', 'w') as wynik:
                    json.dump(stats.high_score, wynik)
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb,
                              shiplives)
            check_bonus_clicked(mouse_x, mouse_y, stats, bonuses1, ai_settings, screen, shiplives, bullets, ship,
                                aliens, sb, lasers)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, lasers)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_bonus_clicked(mouse_x, mouse_y, stats, bonuses1, ai_settings, screen, shiplives, bullets, ship, aliens, sb,
                        lasers):
    if stats.level == 3:
        first_bonus_clicked = bonuses1.msg_font1_rect.collidepoint(mouse_x, mouse_y)
        second_bonus_clicked = bonuses1.msg_font2_rect.collidepoint(mouse_x, mouse_y)
        third_bonus_clicked = bonuses1.msg_font3_rect.collidepoint(mouse_x, mouse_y)
        if first_bonus_clicked:
            ai_settings.bullet_damage = 2
            lasers.empty()
            sleep(1)
            start_new_level(bullets, ai_settings, screen, ship, aliens, stats, sb)
            stats.game_active = True
            stats.bonuses_shown = False
        if second_bonus_clicked:
            stats.ships_left = 4
            shiplives.empty()
            lasers.empty()
            update_lives(screen, ai_settings, shiplives, stats)
            sleep(1)
            start_new_level(bullets, ai_settings, screen, ship, aliens, stats, sb)
            stats.game_active = True
            stats.bonuses_shown = False
        if third_bonus_clicked:
            lasers.empty()
            stats.can_use_laser = True
            sleep(1)
            start_new_level(bullets, ai_settings, screen, ship, aliens, stats, sb)
            stats.game_active = True
            stats.bonuses_shown = False


def flickering_bonueses(shiplives_bonus, bonuses1, stats):
    while stats.bonuses_shown:
        sleep(0.45)
        shiplives_bonus.empty()
        for _ in range(4):
            sleep(0.45)
            bonuses1.add_lives(1)
    return


def check_true_lasers_aliens_collision(true_lasers, aliens, stats):
    for laser in true_lasers:
        collision = pygame.sprite.spritecollide(laser, aliens, True)
        if collision:
            stats.can_use_laser = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, shiplives, planets, stars,
                  bonuses1, shiplives_bonus, aliens_bonus, lasers, true_lasers):
    screen.fill(ai_settings.bg_color)
    stars.draw(screen)
    planets.draw(screen)
    if stats.level == 3 and stats.bonuses_shown and not stats.game_active:
        pygame.mouse.set_visible(True)
        bonuses1.update_first_bonus()
        bonuses1.draw_bonuses()
        shiplives_bonus.draw(screen)
        aliens_bonus.draw(screen)
        lasers.update()
        lasers.draw(screen)
        check_laser_aliens_collision(lasers, aliens_bonus)
        check_laser_height(lasers, bonuses1)
        if not ai_settings.bonuses_flickering:
            ai_settings.bonuses_flickering = True
            p = Thread(target=flickering_bonueses, args=(shiplives_bonus, bonuses1, stats), daemon=True)
            p.start()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    true_lasers.update()
    true_lasers.draw(screen)
    check_true_lasers_aliens_collision(true_lasers, aliens, stats)
    aliens.draw(screen)
    if stats.game_active:
        ship.blitme()
        shiplives.draw(screen)
        sb.show_score()
    for alien in aliens:
        for live in alien.alien_health_bars:
            live.draw_alien_lives()
    if not stats.game_active and not stats.bonuses_shown:
        play_button.draw_button()
    pygame.display.flip()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_texts()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, true_lasers):
    bullets.update()
    for bullet in bullets.copy():
        screen_rect = screen.get_rect()
        if bullet.rect.bottom <= 0 or bullet.rect.x >= screen_rect.right:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, true_lasers)


def check_laser_height(lasers, bonuses1):
    for laser in lasers:
        if laser.rect.y <= 723:
            bonuses1.add_aliens()


def check_laser_aliens_collision(lasers, aliens_bonus):
    for laser in lasers:
        if laser.rect.top == 813:
            aliens_bonus.empty()


def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets, stats, sb, true_lasers):
    collision = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collision:
        for alienss in collision.values():
            for alien in alienss:
                if alien.health != 0:
                    if stats.level != 3:
                        alien.health -= ai_settings.bullet_damage
                        if alien.health <= 0:
                            aliens.remove(alien)
                    else:
                        alien.health -= 2
                        if alien.health <= 0:
                            aliens.remove(alien)
                    alien.alien_health_bars.empty()
                    alien.update_alien_lives()
        if stats.level != 3:
            for aliens in collision.values():
                stats.score += ai_settings.alien_points * len(aliens)
                sb.prep_texts()
            check_high_score(stats, sb)
    if stats.level != 3:
        if len(aliens) == 0:
            sleep(0.5)
            true_lasers.empty()
            start_new_level(bullets, ai_settings, screen, ship, aliens, stats, sb)
    else:
        if len(aliens) == 0:
            new_alien = SuperAlien(screen, ai_settings)
            new_alien.rect.y = 240
            new_alien.rect.x = 610
            new_alien.health = 6
            new_alien.update_alien_lives()
            aliens.add(new_alien)


def start_new_level(bullets, ai_settings, screen, ship, aliens, stats, sb):
    aliens.empty()
    bullets.empty()
    ai_settings.increase_speed()
    stats.level += 1
    if stats.level != 3:
        create_fleet(ai_settings, screen, ship, aliens, stats)
    sb.prep_texts()
    if stats.level == 3:
        stats.bonuses_shown = True
        stats.game_active = False


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, shiplives):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, shiplives)
            break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, shiplives):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        bullets.empty()
        shiplives.empty()
        update_lives(screen, ai_settings, shiplives, stats)
        create_fleet(ai_settings, screen, ship, aliens, stats)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets, shiplives):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    for alien in aliens:
        alien.alien_health_bars.empty()
        alien.update_alien_lives()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, shiplives)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, shiplives)


def fire_bullet(ai_settings, screen, ship, bullets, stats):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship, stats)
        bullets.add(new_bullet)


def get_number_rows(ai_settings, ship_height, alien_height):
    avalible_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avalible_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number, stats):
    if stats.level <= 3:
        alien = Alien(screen, ai_settings)
    elif stats.level <= 6:
        alien = BetterAlien(screen, ai_settings)
    else:
        alien = SuperAlien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.update_alien_lives()
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens, stats):
    if stats.level <= 3:
        alien = Alien(screen, ai_settings)
    elif stats.level <= 6:
        alien = BetterAlien(screen, ai_settings)
    else:
        alien = SuperAlien(screen, ai_settings)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number, stats)


def update_lives(screen, ai_settings, shiplives, stats):
    for live in range(stats.ships_left):
        screen_rect = screen.get_rect()
        shiplive = ShipLives(screen, ai_settings)
        shiplive.rect.x = screen_rect.left + 2 * (shiplive.rect.width - 20) * len(shiplives)
        shiplives.add(shiplive)

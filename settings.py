class Ustawienia():
    def __init__(self, screen):
        self.screen = screen.get_rect()
        self.screen_width = self.screen.width
        self.screen_height = self.screen.height
        self.bg_color = (0, 0, 0)

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.health_color = 29, 97, 102
        self.bullets_allowed = 3

        self.fleet_drop_speed = 7

        self.speedup_scale = 1.02
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.bullet_damage = 1
        self.ship_speed_factor = 2
        self.bullet_speed_factor = 7
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50
        self.ship_limit = 3
        self.bonuses_flickering = False

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
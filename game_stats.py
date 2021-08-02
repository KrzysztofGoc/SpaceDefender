import json


class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        try:
            with open('score.json') as wynik:
                najwyzszy_wynik = json.load(wynik)
                self.high_score = najwyzszy_wynik
        except FileNotFoundError:
            self.high_score = 0

    def reset_stats(self):
        self.can_use_laser = False
        self.game_active = False
        self.bonuses_shown = False
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

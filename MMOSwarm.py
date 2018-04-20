import random
from enum import Enum


def expression(values):
    return values['x']*values['x'] + values['y']*values['y']

class Ranks(Enum):
    GRANDMASTER = 1
    MASTER = 2
    DIAMOND = 3
    GOLD = 4
    SILVER = 5
    BRONZE = 6
    UNSKILLED = 7


class RankSize(Enum):
    GRANDMASTER = pow(2, Ranks.GRANDMASTER.value)
    MASTER = pow(2, Ranks.MASTER.value)
    DIAMOND = pow(2, Ranks.DIAMOND.value)
    GOLD = pow(2, Ranks.GOLD.value)
    SILVER = pow(2, Ranks.SILVER.value)
    BRONZE = pow(2, Ranks.BRONZE.value) * 3 / 4
    UNSKILLED = pow(2, Ranks.BRONZE.value)


class Player:
    def __init__(self):
        self.current = dict()
        self.best = dict()


class MMOpso:
    def __init__(self):
        self.player_base = []
        self.player_base_size = pow(2, Ranks.BRONZE.value)
        self.x_max_range = 10
        self.x_min_range = -10
        self.y_max_range = 10
        self.y_min_range = -10
        self.expression = expression

        self.x_width = self.x_max_range - self.x_min_range
        self.y_width = self.y_max_range - self.y_min_range

        for index in range(self.player_base_size):
            player_info = Player()
            player_info.current['x'] = random.random() * self.x_width + self.x_min_range
            player_info.current['y'] = random.random() * self.y_width + self.y_min_range
            player_info.current['value'] = self.expression(player_info.current)
            player_info.best['x'] = player_info.current['x']
            player_info.best['y'] = player_info.current['y']
            player_info.best['value'] = player_info.current['value']
            self.player_base.append(player_info)

        for p in self.player_base:
            print(p.current)

if __name__ == '__main__':
    MMOpso()


import random
from enum import Enum


def expression(values):
    #return values['x']*values['x'] + values['y']*values['y']
    return (values['x'] - 1) *(values['x'] - 1) + values['y'] * values['y']

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

    def __str__(self):
        return "current: %s, best: %s \n" % (self.current, self.best)

    def __float__(self):
        if self.current['value'] is not None:
            return self.current['value']
        else:
            raise ValueError

    def __gt__(self, other):
        return self.current['value'] > other.current['value']

class MMOpso:
    gauss_arg1 = 0
    gauss_arg2 = 0.5

    def __init__(self):
        self.player_base = list()
        self.player_base_size = pow(2, Ranks.BRONZE.value)
        self.best_found = dict()
        self.x_max_range = 10
        self.x_min_range = -10
        self.y_max_range = 10
        self.y_min_range = -10
        self.team_size = 5
        self.expression = expression

        self.x_width = self.x_max_range - self.x_min_range
        self.y_width = self.y_max_range - self.y_min_range

    def populate(self):
        for index in range(self.player_base_size):
            player_info = Player()
            player_info.current['x'] = random.random() * self.x_width + self.x_min_range
            player_info.current['y'] = random.random() * self.y_width + self.y_min_range
            player_info.current['value'] = self.expression(player_info.current)
            player_info.best['x'] = player_info.current['x']
            player_info.best['y'] = player_info.current['y']
            player_info.best['value'] = player_info.current['value']
            self.player_base.append(player_info)
        self.best_found['x'] = self.player_base[0].current['x']
        self.best_found['y'] = self.player_base[0].current['y']
        self.best_found['value'] = self.player_base[0].current['value']
        self._update_values()

    @staticmethod
    def _is_better(arg1, arg2):
        if arg1 < arg2:
            return True
        else:
            return False

    def _update_values(self):
        for player in self.player_base:
            player.current['value'] = self.expression(player.current)
            if self._is_better(player.current['value'], player.best['value']):
                player.best['value'] = player.current['value']
                player.best['x'] = player.current['x']
                player.best['y'] = player.current['y']
                if self._is_better(player.best['value'], self.best_found['value']):
                    self.best_found['value'] = player.best['value']
                    self.best_found['x'] = player.best['x']
                    self.best_found['y'] = player.best['y']

    def _sort(self):
        self.player_base[0 : RankSize.SILVER.value].sort()

    def best_found_value(self):
        return self.best_found['value']

    def print_best(self):
        print("Best:\nX: %s\nY: %s\nValue: %s\n-----" % (self.best_found['x'], self.best_found['y'], self.best_found['value']))

    @staticmethod
    def _move_by_vector(player, vector):
        player.current['x'] = random.gauss(MMOpso.gauss_arg1, MMOpso.gauss_arg2) * 2 * vector['x'] + player.current['x']
        player.current['y'] = random.gauss(MMOpso.gauss_arg1, MMOpso.gauss_arg2) * 2 * vector['y'] + player.current['y']

    def _master_move(self, player):
        vector = dict()
        vector['x'] = player.current['x'] - player.best['x']
        vector['y'] = player.current['y'] - player.best['y']
        MMOpso._move_by_vector(player, vector)

    def _bronze_move(self, player):
        vector = dict()
        vector['x'] = player.current['x'] - self.player_base[0].current['x']
        vector['y'] = player.current['y'] - self.player_base[0].current['y']
        MMOpso._move_by_vector(player, vector)

    def _team_move(self, team):
        best = team[0]
        for player in team:
            if self._is_better(player.current['value'], best.current['value']):
                best = player

        for player in team:
            vector = dict()
            vector['x'] = best.current['x'] - player.current['x']
            vector['y'] = best.current['y'] - player.current['y']
            MMOpso._move_by_vector(player, vector)

    def _move_players(self):
        for index in range(self.player_base_size):
            if index <= RankSize.GRANDMASTER.value:
                self._master_move(self.player_base[index])
            elif index <= RankSize.MASTER.value:
                self._master_move(self.player_base[index])
            elif RankSize.SILVER.value < index <= RankSize.BRONZE.value:
                self._bronze_move(self.player_base[index])
            else:
                teams = self._matchmaking()
                for team in teams:
                    self._team_move(team)

    # returns list of teams (5 players)
    def _matchmaking(self):
        diamond = list()
        for player in self.player_base[RankSize.MASTER.value : RankSize.DIAMOND.value]:
            diamond.append(player)
        gold = list()
        for player in self.player_base[RankSize.DIAMOND.value: RankSize.GOLD.value]:
            gold.append(player)
        silver = list()
        for player in self.player_base[RankSize.GOLD.value: RankSize.SILVER.value]:
            silver.append(player)

        players_to_match = [list(), list(), list()]
        players_to_match[0] = diamond
        players_to_match[1] = gold
        players_to_match[2] = silver
        rank = 0
        teams_chosen = list()
        while rank < len(players_to_match):
            team = list()
            while len(team) < self.team_size:
                if len(players_to_match[rank]) == 0:
                    rank += 1
                    if rank >= len(players_to_match):
                        break
                index = random.randint(0, len(players_to_match[rank]) - 1)
                team.append(players_to_match[rank].pop(index))
            teams_chosen.append(team)

        return teams_chosen

    def next_iteration(self):
        self._sort()
        self._move_players()
        self._update_values()


    #TODO
    # match tries to find ppl on the same rank first. if not possible tries other ranks. create lists of not chosen
    # players. One list per rank. delete player that is chosen.






    def _match_and_move_players(self):
        players_to_pick = [1] * Ranks.SILVER.value
        for i in range(len(players_to_pick)):
            if i <= Ranks.MASTER.value:
                continue
            elif players_to_pick[i] == 1:
                match = self._matchmaking(i, players_to_pick)







if __name__ == '__main__':
    pso = MMOpso()
    pso.populate()
    for i in range(100):
        pso.next_iteration()
    pso.print_best()


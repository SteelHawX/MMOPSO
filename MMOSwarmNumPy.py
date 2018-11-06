import random
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

np.random.seed(1)

def expression(values):
    result = 0
    for x in values:
        result += x**2
    return result


class Ranks(Enum):
    GRANDMASTER = 1
    MASTER = 2
    DIAMOND = 3
    GOLD = 4
    SILVER = 5
    BRONZE = 6

class RankSize(Enum):
    GRANDMASTER = np.power(2, Ranks.GRANDMASTER.value)
    MASTER = np.power(2, Ranks.MASTER.value)
    DIAMOND = np.power(2, Ranks.DIAMOND.value)
    GOLD = np.power(2, Ranks.GOLD.value)
    SILVER = np.power(2, Ranks.SILVER.value)
    BRONZE = np.power(2, Ranks.BRONZE.value)

"""class Player:
    def __init__(self):
        self.current = np.array()
        self.best = np.array()

    def __str__(self):
        return "current: %s, best: %s \n" % (self.current, self.best)

    def __float__(self):
        if self.current[-1] is not None:
            return self.current[-1]
        else:
            raise ValueError

    def __gt__(self, other):
        return self.current[-1] > other.current[-1]
"""

    
class MMOpso:
    gauss_arg1 = 0
    gauss_arg2 = 0.5

    def __init__(self, expression, dimensions, min_range, max_range, findMin = True):
        self.player_base_size = RankSize.SILVER.value #BRONZE
        self.player_base_current = np.empty((dimensions+1, self.player_base_size))
        self.player_base_best = np.empty((dimensions+1, self.player_base_size))
        self.min_range = np.full(dimensions, min_range)
        self.max_range = np.full(dimensions, max_range)
        self.team_size = 5
        self.dimensions = dimensions
        self.player_dim = self.dimensions + 1
        self.expression = expression
        if findMin:
            self.return_best = np.argmin
            self._is_better = lambda arg1, arg2: arg1 < arg2
        else:
            self.return_best = np.argmax
            self._is_better = lambda arg1, arg2: arg1 > arg2

        self.best_found_log = list()

        self.range_width = np.array(max_range - min_range)

        self._initialize_values()
        self._sort()

    def best_values(self):
        print_text = "BEST VALUES\n"
        index = 1
        for player in self.player_base_best.transpose():
            print_text += f"player {index} : {player[-1]:.6f}\n"
            index += 1
        return print_text

    def current_values(self):
        print_text = "CURRENT VALUES\n"
        index = 1
        for player in self.player_base_current.transpose():
            print_text += f"player {index} : {player[-1]:.6f}\n"
            index += 1
        return print_text
    
    def best_positions(self):
        print_text = "BEST POSITIONS\n"
        index = 1
        for player in self.player_base_best.transpose():
            print_text += f"player {index} : "
            for dimension in player[:-1]:
                print_text += f"{dimension:.6f} "
            print_text += "\n"
            index += 1
        return print_text

    def current_positions(self):
        print_text = "CURRENT POSITIONS\n"
        index = 1
        for player in self.player_base_current.transpose():
            print_text += f"player {index} : "
            for dimension in player[:-1]:
                print_text += f"{dimension:.6f} "
            print_text += "\n"
            index += 1
        return print_text

    def _initialize_values(self):
        #initialize CURRENT positions of every player
        self.player_base_current[:-1] = (self.range_width.dot(np.random.rand(self.dimensions, self.player_base_size)).transpose() + self.min_range).transpose()
        #print(np.shape(self.player_base_current))
        
        #initialize CURRENT values of every player
        for player in self.player_base_current.transpose():
            player[-1] = expression(player[:-1])
        
        #initialize BEST positions and values; in t(0) it equals CURRENT
        self.player_base_best = np.copy(self.player_base_current)
        
        #initalize BEST PLAYER (positions + value)
        index_of_best = self.return_best(self.player_base_best.transpose()[-1])
        self.best_found = np.copy(self.player_base_best.transpose()[index_of_best])
        self._append_best_found_log()
    
    def _find_best(self):
        index_of_best = self.return_best(self.player_base_best.transpose()[-1])
        best_in_current = self.player_base_best.transpose()[index_of_best]
        if self._is_better(best_in_current[-1], self.best_found[-1]):
            self.best_found = np.copy(best_in_current)
        self._append_best_found_log()

    def _update_values(self):
        for player in self.player_base_current.transpose():
            player[-1] = expression(player[:-1])


        for index in range(self.player_base_size):
            if self._is_better(self.player_base_current[-1][index], self.player_base_best[-1][index]):
                #print((self.player_base_current[-1][index], self.player_base_best[-1][index]))
                self.player_base_best.transpose()[index] = np.copy(self.player_base_current.transpose()[index])


    def _append_best_found_log(self):
        self.best_found_log.append(self.best_found)
    
    def _sort(self):
        best_n_current = np.concatenate((self.player_base_best, self.player_base_current), axis=0).transpose()
        best_n_current = best_n_current[best_n_current[:,-1].argsort()]
        split = np.array_split(best_n_current, 2, axis=1)
        self.player_base_best = split[0].transpose()
        self.player_base_current = split[1].transpose()


    def _matchmaking(self):
        #should be sorted
        player_base_t = self.player_base_current.transpose()
        diamond = [np.empty(self.player_dim)]
        for player in player_base_t[RankSize.MASTER.value : RankSize.DIAMOND.value]:
            diamond = np.append(diamond, [player], axis=0)
        gold = [np.empty(self.player_dim)]
        for player in player_base_t[RankSize.DIAMOND.value : RankSize.GOLD.value]:
            gold = np.append(gold, [player], axis=0)
        silver = [np.empty(self.player_dim)]
        for player in player_base_t[RankSize.GOLD.value : RankSize.SILVER.value]:
            silver = np.append(silver, [player], axis=0)
        players_to_match = [diamond, gold, silver]
        
        rank = 0 # first index of players_to_match
        teams_chosen = [np.empty((self.team_size, self.player_dim))]
        teams_chosen_index = 0
        while rank < len(players_to_match):
            current_team_size = 0
            team = [np.empty(self.player_dim)]
            while current_team_size < self.team_size:
                if len(players_to_match[rank]) == 0:
                    rank += 1
                if rank >= len(players_to_match) or len(players_to_match[rank]) == 0:
                    break
                player_chosen_index = np.random.randint(0, len(players_to_match[rank]))
                if current_team_size == 0:
                    team = [players_to_match[rank][player_chosen_index]]
                else:
                    team = np.append(team, [players_to_match[rank][player_chosen_index]], axis=0)
                players_to_match[rank] = np.delete(players_to_match[rank], player_chosen_index, axis=0)
                current_team_size += 1
            if current_team_size == self.team_size:
                if teams_chosen_index == 0:
                    teams_chosen = [team]
                else:
                    teams_chosen = np.append(teams_chosen, [team], axis=0)
        # returns array of shape(x, team_size, player_dim) where x is number of teams created 
        return teams_chosen

    def _move_players(self):
        for index in range(self.player_base_size):
            if index <= RankSize.GRANDMASTER.value:
                self.player_base_current.transpose()[index] = self._master_move(self.player_base_current.transpose()[index], index)
            elif index <= RankSize.MASTER.value:
                self.player_base_current.transpose()[index] = self._master_move(self.player_base_current.transpose()[index], index)
            elif RankSize.SILVER.value < index <= RankSize.BRONZE.value:
                self.player_base_current.transpose()[index] = self._bronze_move(self.player_base_current.transpose()[index])        
        teams = self._matchmaking()
        for teamIndex in range(len(teams)):
            teams[teamIndex] = self._team_move(teams[teamIndex])
        teamIndex = 0
        playerIndex = 0
        maxIndex = 0
        if self.player_base_size < RankSize.SILVER.value:
            maxIndex = self.player_base_size
        for index in range(RankSize.MASTER.value, maxIndex):
            if playerIndex == len(teams[teamIndex]):
                playerIndex = 0
                teamIndex += 1
            self.player_base_current.transpose()[index] = teams[teamIndex][playerIndex]
            playerIndex += 1
                

    def _move_by_vector(self, player, vector):
        mod = np.random.normal(self.gauss_arg1, self.gauss_arg2, self.player_dim)
        #mod = np.full(self.player_dim, 0.5)
        mod = np.multiply(mod, 2)
        print("Move by vector")
        print(mod)
        mod[-1] = 0
        print(f'Raw vector: {vector}')
        vector = np.multiply(vector, mod)
        print(f'Modded vector: {vector}')
        print(f'Raw player: {player}')
        player = np.add(player, vector)
        print(f'Modded player: {player}')
        return player
        

    def _master_move(self, player, index):
        #print(f'player: {player}')
        #print(f'player2: {player}')
        vector = np.subtract(self.player_base_best.transpose()[index], player)
        player = self._move_by_vector(player, vector)
        print(player)
        return player

    def _bronze_move(self, player):
        vector = np.subtract(self.player_base_current.transpose()[0], player)
        player =  self._move_by_vector(player, vector)
        return player

    def _team_move(self, team):
        best = team[0]
        for player in team:
            if self._is_better(player[-1], best[-1]):
                best = player
        for index in range(len(team)):
            vector = np.subtract(best, team[index])
            team[index] = self._move_by_vector(team[index], vector)
        #print(f"PLAYER AFTER\n{team[4]}")
        return team    
            

    def next_iteration(self):
        #print("NOT SORTED")
        #print(self.current_positions())
        #print(self.current_values())
        self._sort()
        #print("SORTED")
        #print(self.best_positions())
        #print(self.best_values())
        self._move_players()
        #print("MOVED")
        #print(self.current_positions())
        self._update_values()
        #print("UPDATED")
        #print(self.current_values())
        #print(self.best_values())
        self._find_best()
        self._append_best_found_log()
        #print(self.best_values())

    def plot(self, start_idx = 0, end_idx = -1):
        best_value_found_log = list()
        for val in self.best_found_log[start_idx : end_idx]:
            best_value_found_log.append(val[-1])
        print("BEST FOUND VALUE")
        print(best_value_found_log)
        plt.plot(best_value_found_log)
        plt.show()

    def get_players(self):
        return self.player_base_current


if __name__ == '__main__':
    pso = MMOpso(expression, 2, -10, 10)
    for i in range(3):
        #print(pso.best_values())
        print(pso.player_base_current.transpose()[0])
        pso.next_iteration()
    #pso.plot()


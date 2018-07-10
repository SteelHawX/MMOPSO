import random
import numpy as np
from enum import Enum

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
        self.player_base_size = RankSize.DIAMOND.value #BRONZE
        self.player_base_current = np.empty((dimensions+1, self.player_base_size))
        self.min_range = np.full(dimensions, min_range)
        self.max_range = np.full(dimensions, max_range)
        self.team_size = 5
        self.dimensions = dimensions
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

    def _initialize_values(self):
        #initialize CURRENT positions of every player
        self.player_base_current[:-1] = (self.range_width.dot(np.random.rand(self.dimensions, self.player_base_size)).transpose() + self.min_range).transpose()
        
        #initialize CURRENT values of every player
        for player in self.player_base_current.transpose():
            player[-1] = expression(player[:-1])
        
        #initialize BEST positions and values; in t(0) it equals CURRENT
        self.player_base_best = np.copy(self.player_base_current)
        
        #initalize BEST PLAYER (positions + value)
        index_of_best = self.return_best(self.player_base_best[-1])
        self.best_found = np.copy(self.player_base_best.transpose()[index_of_best])
        self._append_best_found_log()
    
    def _find_best(self):
        index_of_best = self.return_best(self.player_base_best[-1])
        best_in_current = self.player_base_best.transpose()[index_of_best]
        if self._is_better(best_in_current[-1], self.best_found[-1]):
            self.best_found = np.copy(best_in_current)
        self._append_best_found_log()

    def _append_best_found_log(self):
        self.best_found_log.append(self.best_found)
    
    def _sort(self):
        #probably concatenate current and best -> sort -> split



if __name__ == '__main__':
    pso = MMOpso(expression, 10, -10, 10)

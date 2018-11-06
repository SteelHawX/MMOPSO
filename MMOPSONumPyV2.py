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

class MMOpso:
	gauss_arg1 = 0
	gauss_arg2 = 0.5

	def __init__(self, expression, dimension, min_range, max_range, find_min = True, player_base_size = RankSize.SILVER.value, team_size = 5):
		self.player_base_size = player_base_size
		self.dimension = dimension
		self.team_size = team_size
		self.expression = expression

		self.player_base_current = np.empty((self.player_base_size, self.dimension+1))
		self.player_base_best = np.copy(self.player_base_current)
		self.min_range = np.full(dimension, min_range)
		self.max_range = np.full(dimension, max_range)

		if find_min:
			self.return_best = np.argmin
			self._is_better = lambda arg1, arg2: arg1 < arg2
		else:
			self.return_best = np.argmax
			self._is_better = lambda arg1, arg2: arg1 > arg2

		self.best_found_log = list()

		self.range_width = np.array(max_range - min_range)

		self._initialize_values()
		#self._sort()

	def best_values(self):
		print_text = "BEST VALUES\n"
		index = 1
		for player in self.player_base_best:
			print_text += f"player {index} : {player[-1]:.6f}\n"
			index += 1
		return print_text

	def current_values(self):
		print_text = "CURRENT VALUES\n"
		index = 1
		for player in self.player_base_current:
			print_text += f"player {index} : {player[-1]:.6f}\n"
			index += 1
		return print_text

	def best_positions(self):
		print_text = "BEST POSITIONS\n"
		index = 1
		for player in self.player_base_best:
			print_text += f"player {index} : "
			for dimension in player[:-1]:
				print_text += f"{dimension:.6f} "
			print_text += "\n"
			index += 1
		return print_text

	def current_positions(self):
		print_text = "CURRENT POSITIONS\n"
		index = 1
		for player in self.player_base_current:
			print_text += f"player {index} : "
			for dimension in player[:-1]:
				print_text += f"{dimension:.6f} "
			print_text += "\n"
			index += 1
		return print_text

	def _initialize_values(self):
		# initialize CURRENT positions of every player
		self.player_base_current[:][:-1] = (self.range_width.dot(np.random.rand(self.player_base_size, self.dimension)) + self.min_range)


if __name__ == '__main__':
	pso = MMOpso(expression, 2, -10, 10)
	print(pso.current_positions())


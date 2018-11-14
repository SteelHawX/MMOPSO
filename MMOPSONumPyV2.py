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

		# represents matrix where first index is the index of player and the second is the dimension ( in case of the last value its expression value)
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

	def _transpose_player_base(self):
		return self.player_base_current.transpose()

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

	def _append_best_found_log(self):
		self.best_found_log.append(self.best_found)

	def _initialize_values(self):
		# initialize CURRENT positions of every player
		t_player_base = self._transpose_player_base()
		print(np.shape(t_player_base[:][:-1]))
		t_player_base[:][:-1] = np.random.rand(self.dimension, self.player_base_size).dot(self.range_width)
		t_player_base[:][:-1] = (t_player_base[:][:-1].transpose() + self.min_range).transpose()

		# initialize CURRENT values of every player
		for player in self.player_base_current:
			player[-1] = expression(player[:-1])

		# initialize BEST positions and values; in t(0) it equals CURRENT
		self.player_base_best = np.copy(self.player_base_current)

		# initalize BEST PLAYER (positions + value)
		index_of_best = self.return_best(t_player_base[-1])
		self.best_found = np.copy(self.player_base_best[index_of_best])
		self._append_best_found_log()

	def _find_best(self):
		t_player_base = self._transpose_player_base()
		index_of_best = self.return_best(t_player_base[-1])
		best_in_current= np.copy(self.player_base_best[index_of_best])
		if self._is_better(best_in_current[-1], self.best_found[-1]):
			self.best_found = np.copy(best_in_current)
		self._append_best_found_log()

	def _update_values(self):
		for player in self.player_base_current:
			player[-1] = expression(player[:-1])

		for index in range(self.player_base_size):
			#print(index)
			if self._is_better(self.player_base_current[index][-1], self.player_base_best[index][-1]):
				#print(self.player_base_current[index])
				self.player_base_best[index] = np.copy(self.player_base_current[index])

	def _append_best_found_log(self):
		self.best_found_log.append(self.best_found)

	def _sort(self):
		best_current_concat = np.concatenate((self.player_base_current, self.player_base_best), axis=1)
		best_current_concat = best_current_concat[best_current_concat[:,-1].argsort()]
		best_current_split = np.array_split(best_current_concat, 2, axis = 1)
		self.player_base_current = best_current_split[0]
		self.player_base_best = best_current_split[1]

if __name__ == '__main__':
	pso = MMOpso(expression, 2, -10, 10)
	#print(pso.current_positions())
	#print(pso.current_values())
	pso._update_values()
	pso._sort()
	print(pso.current_positions())
	print(pso.current_values())


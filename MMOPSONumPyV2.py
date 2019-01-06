import random
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

np.random.seed(1)

def simple(values):
	result = 0
	for x in values:
		result += x**2
	return result

def rosenbrock(values):
	result = 0
	counter = 0
	prev_x = 0
	for x in values:
		if counter != 0:
			result += (1 - prev_x)*(1 - prev_x) + 100*(x - prev_x*prev_x)*(x - prev_x*prev_x)
		prev_x = x
		counter += 1
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
	gauss_arg1 = 0.5
	gauss_arg2 = 0.5

	def __init__(self, expression, dimension, min_range, max_range, find_min = True, player_base_size = RankSize.BRONZE.value, team_size = 5):
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
			player[-1] = self.expression(player[:-1])

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
			player[-1] = self.expression(player[:-1])

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

	def _index_shift(self, players_chosen, index) -> int:

		counter = 0
		print(f"Table: {players_chosen}")
		print(f"Index: {index}")
		for player in players_chosen[:index]:
			if player == 1:
				counter += 1
		print(f"After first part {counter}")
		if(players_chosen[index] == 1):
			idx = index + 1
			while idx < len(players_chosen) and players_chosen[idx] == 1:
				counter += 1
				idx += 1
			print(f"After second part {counter}")
		print(f"Shift: {counter}")
		return int(counter)

	def _index_shift_v2(self, players_chosen, index) -> int:
		zero_counter = -1
		idx = 0
		#print(f"Table: {players_chosen}")
		#print(f"Index: {index}")
		while zero_counter < index and idx < len(players_chosen):
			if players_chosen[idx] == 0:
				zero_counter += 1
			idx += 1
		idx -= 1
		#print(f"Shift: {idx}")
		return idx


	def _matchmaking(self):
		#playerbase should be sorted

		offset = [RankSize.MASTER.value, RankSize.DIAMOND.value, RankSize.GOLD.value, RankSize.SILVER.value]
		diamond_players = self.player_base_current[RankSize.MASTER.value : RankSize.DIAMOND.value]
		gold_players = self.player_base_current[RankSize.DIAMOND.value : RankSize.GOLD.value]
		silver_players = self.player_base_current[RankSize.GOLD.value : RankSize.SILVER.value]
		players_to_match = np.copy([diamond_players, gold_players, silver_players])

		rank = 0 # first index of players_to_match
		ready_teams_counter = 0
		ready_teams_max = int((offset[-1] - offset[0])/self.team_size)
		ready_teams = np.empty((ready_teams_max, self.team_size))
		max_rank = len(players_to_match)
		players_chosen = [0] * (offset[rank + 1] - offset[rank])
		while rank < max_rank:
			draft_team_size = 0
			draft_team = np.zeros(self.team_size)
			#print(players_chosen)
			while draft_team_size < self.team_size:
				#print('----')
				#if rank >= max_rank or len(players_to_match[rank]) == 0:
				#	break
				#elif len(players_to_match[rank]) == 0:

				player_chosen_index = np.random.randint(0, len(players_to_match[rank]))

				players_to_match[rank] = np.delete(players_to_match[rank], player_chosen_index, axis=0)
				player_chosen_index = self._index_shift_v2(players_chosen, player_chosen_index)
				#print(f"pc_idx: {player_chosen_index}")
				players_chosen[player_chosen_index] = 1

				draft_team[draft_team_size] = offset[rank] + player_chosen_index
				draft_team_size += 1

				if len(players_to_match[rank]) == 0:
					rank += 1
					if rank < max_rank:
						players_chosen = [0] * (offset[rank + 1] - offset[rank])
						#print("reset")
					else:
						break
			if draft_team_size == self.team_size:
				ready_teams[ready_teams_counter] = draft_team
				ready_teams_counter += 1
		return ready_teams

	def _move_by_vector(self, player_index, vector):
		#print(vector)
		mod = np.random.normal(self.gauss_arg1, self.gauss_arg2, self.dimension + 1)
		mod = np.multiply(mod, 2)
		mod[-1] = 0
		#print(mod)
		vector = np.multiply(vector, mod)
		#print(self.player_base_current[player_index])
		#print(vector)
		#print(vector)
		self.player_base_current[player_index] = np.add(self.player_base_current[player_index], vector)

	def _move_players(self):
		for index in range(self.player_base_size):
			if index < RankSize.GRANDMASTER.value:
				self._master_move(index, index)
			elif index < RankSize.MASTER.value:
				self._master_move(index, index)
			elif RankSize.SILVER.value <= index < RankSize.BRONZE.value:
				self._bronze_move(index)
		teams = self._matchmaking()
		for index in range(len(teams)):
			self._team_move(teams[index])

	def _team_move(self, team):
		#print(team)
		#print('-')
		best = self.player_base_current[int(team[0])]
		best_index = int(team[0])
		#print(best)
		for player_index in team:
			#print(self.player_base_current[int(player_index)])
			if self._is_better(self.player_base_current[int(player_index)][-1], best[-1]):
				#print('New best')
				best = self.player_base_current[int(player_index)]
				best_index = int(player_index)
		for player_index in team:
			#print('Before')
			#print( self.player_base_current[int(player_index)])
			vector = np.subtract(best, self.player_base_current[int(player_index)])
			self._move_by_vector(int(player_index), vector)

	def _master_move(self, player_index, master_index):
		if player_index == master_index:
			self._self_move(player_index)
		vector = np.subtract((self.player_base_current[master_index]), self.player_base_current[player_index])
		self._move_by_vector(player_index, vector)

	def _bronze_move(self, player_index):
		self._master_move(player_index, 0)

	def _self_move(self, player_index):
		vector = np.subtract(self.player_base_best[player_index], self.player_base_current[player_index])
		self._move_by_vector(player_index, vector)

	def next_iteration(self):
		self._sort()
		self._move_players()
		self._update_values()
		self._find_best()
		self._append_best_found_log()


if __name__ == '__main__':
	pso = MMOpso(rosenbrock, 10, -10, 10)
	for i in range(100000):
		pso.next_iteration()
	print(pso.best_found_log[-1])
	#print(rosenbrock([0,0,0,0,0,0,0,0,0,0]))



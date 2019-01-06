import numpy as np
import MMOPSONumPyV2 as mmo

np.random.seed(1)

class BasicPSO:
    def __init__(self, expression, dimension, min_bound, max_bound):
        self.expression = expression
        self.dimension = dimension
        self.size = pow(2, 6)
        self.particle_bias = 0.5
        self.global_bias = 0.5
        self.velocity_mult = 0.5

        self.particles_current = np.empty((self.size, self.dimension + 1))
        self.particles_best = np.copy(self.particles_current)
        self.velocity = np.empty((self.size, self.dimension))
        self.min_bound = np.full(self.dimension, min_bound)
        self.max_bound = np.full(self.dimension, max_bound)

        self.return_best = np.argmin
        self._is_better = lambda arg1, arg2: arg1 < arg2

        self.best_found_log = list()
        self.range_width = np.array(max_bound - min_bound)

        self._initialize_values()

    def _initialize_values(self):
        t_particles = self.particles_current.transpose()
        #print(np.shape(t_particles[:][:-1]))
        t_particles[:][:-1] = np.random.rand(self.dimension, self.size).dot(self.range_width)
        t_particles[:][:-1] = (t_particles[:][:-1].transpose() + self.min_bound).transpose()

        t_velocity = self.velocity.transpose()
        t_velocity[:][:] = np.random.rand(self.dimension, self.size).dot(self.range_width)
        t_velocity[:][:] = (t_velocity[:][:].transpose() + self.min_bound).transpose()


        for particle in self.particles_current:
            particle[-1] = self.expression(particle[:-1])

        self.particles_best = np.copy(self.particles_current)

        #print(self.particles_best)


        index_of_best = self.return_best(t_particles[-1])
        self.best_found = np.copy(self.particles_best[index_of_best])
        self.best_found_log.append(self.best_found)
        #print(self.best_found_log)

    def _find_best(self):
        t_particles = self.particles_current.transpose()
        index_of_best = self.return_best(t_particles[-1])
        currently_best = np.copy(self.particles_best[index_of_best])
        if self._is_better(currently_best[-1], self.best_found[-1]):
            self.best_found = np.copy(currently_best)
        self.best_found_log.append(self.best_found)

    def _update_values(self):
        for particle in self.particles_current:
            particle[-1] = self.expression(particle[:-1])

        for idx in range(self.size):
            if self._is_better(self.particles_current[idx][-1], self.particles_best[idx][-1]):
                self.particles_best[idx] = np.copy(self.particles_current[idx])

    def _update_velocity(self):
        #print(self.velocity)
        self.velocity *= self.velocity_mult
        #print(self.velocity)
        diff = self.particles_best.transpose()[:-1] - self.particles_current.transpose()[:1]
        #
        #print('---------------')
        best_array = self.best_found[:-1]
        for i in range(self.size - 1):
            best_array = np.vstack((best_array, self.best_found[:-1]))
        best_diff = best_array.transpose() - self.particles_current.transpose()[:-1]
        self.velocity = (self.velocity.transpose() + np.random.rand(self.dimension, self.size) * self.particle_bias * diff).transpose()
        self.velocity = (self.velocity.transpose() + np.random.rand(self.dimension, self.size) * self.global_bias * best_diff).transpose()

    def _move_particles(self):
        #print('----')
        self.particles_current.transpose()[:-1] = self.particles_current.transpose()[:-1] + self.velocity.transpose()
        #print(self.particles_current)

    def next_iteration(self):
        self._update_velocity()
        self._move_particles()
        self._update_values()
        self._find_best()

    def print_all(self):
        print('Current')
        print(self.particles_current)
        print('Velocity')
        print(self.velocity)
        print('Best')
        print(self.particles_best)

if __name__ == '__main__':
    pso = BasicPSO(mmo.simple, 2, -10, 10)
    for i in range(1000):
        pso.next_iteration()
        if not i%50:
            print(pso.best_found_log[-1])


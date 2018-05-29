import random
import matplotlib.pyplot as plt


class Particle:
    def __init__(self):
        self.current = dict()
        self.velocity = dict()
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

class BASICpso:
    def __init__(self, expr):
        self.particle_base = list()
        self.particle_base_size = pow(2, 6)
        self.best_found = dict()
        self.x_max_range = 10
        self.x_min_range = -10
        self.y_max_range = 10
        self.y_min_range = -10
        self.expression = expr
        self.particle_bias = 0.5
        self.global_bias = 0.5
        self.velocity_mult = 0.5
        self.best_found_log = list()

        self.x_width = self.x_max_range - self.x_min_range
        self.y_width = self.y_max_range - self.y_min_range
        
        
    def populate(self):
        for index in range(self.particle_base_size):
            particle_info = Particle()
            particle_info.current['x'] = random.random() * self.x_width + self.x_min_range
            particle_info.current['y'] = random.random() * self.y_width + self.y_min_range
            particle_info.current['value'] = self.expression(particle_info.current)
            particle_info.velocity['x'] = random.random() * self.x_width * 2 - self.x_width
            particle_info.velocity['y'] = random.random() * self.y_width * 2 - self.y_width
            particle_info.best['x'] = particle_info.current['x']
            particle_info.best['y'] = particle_info.current['y']
            particle_info.best['value'] = particle_info.current['value']
            self.particle_base.append(particle_info)
        self.best_found['x'] = self.particle_base[0].current['x']
        self.best_found['y'] = self.particle_base[0].current['y']
        self.best_found['value'] = self.particle_base[0].current['value']
        self._update_values()

    def _update_velocity(self):
        for particle in self.particle_base:
            for dimension in particle.velocity:  # type: str
                particle_randomizer = random.random()
                global_randomizer = random.random()
                particle.velocity[dimension] *= self.velocity_mult
                particle.velocity[dimension] += self.particle_bias * particle_randomizer * (particle.best[dimension] - particle.current[dimension])
                particle.velocity[dimension] += self.global_bias * global_randomizer * (self.best_found[dimension] - particle.current[dimension])

    def _update_values(self):
        self._update_velocity()
        self._move_particles()

    def _move_particles(self):
        for particle in self.particle_base:
            for dimension in particle.velocity:
                if dimension is not 'value':
                    particle.current[dimension] += particle.velocity[dimension]
            particle.current['value'] = self.expression(particle.current)
            if self._is_better(particle.current['value'], particle.best['value']):
                for dimension in particle.best:
                    particle.best[dimension] = particle.current[dimension]
                if self._is_better(particle.current['value'], self.best_found['value']):
                    for dimension in self.best_found:
                        self.best_found[dimension] = particle.current[dimension]
        self.best_found_log.append(self.best_found['value'])
        
    def next_iteration(self):
        self._update_values()
        
    
    @staticmethod
    def _is_better(arg1, arg2):
        if arg1 < arg2:
            return True
        else:
            return False

    def best_found_value(self):
        return self.best_found['value']

    def print_best(self):
        print("Best:\nX: %s\nY: %s\nValue: %s\n-----" % (self.best_found['x'], self.best_found['y'], self.best_found['value']))

    def plot(self, start_idx=0, end_idx=-1):
        plt.plot(self.best_found_log[start_idx: end_idx])
        plt.xlabel("iteration")
        plt.ylabel("best found")
        plt.show()

if __name__ == "__main__":
    def expression(values):
        # return values['x']*values['x'] + values['y']*values['y']
        return (values['x'] - 1) * (values['x'] - 1) + values['y'] * values['y']
    pso = BASICpso(expression)
    pso.populate()
    for i in range(100):
        pso.next_iteration()
    pso.print_best()
    pso.plot()
"""Genetic algorithm using roulette selection, crossover, and mutation"""
import itertools
import random


class Permutation(object):
    """Represents a list of integers"""
    def __init__(self, N: int, arrangement: list, fitness: int=0):
        self.population_size = N
        self.fitness = fitness or 0
        self.arrangement = arrangement


class GoalFound(Exception):
    pass


class GeneticAlgorithm(object):
    """index: row, value: row"""
    def __init__(self, N: int):
        self.population_size = N
        self.goal_fitness = (self.population_size - 1) * self.population_size
        self.board = list(range(self.population_size))
        self.permutations = []
        arrangement = list(range(self.population_size))
        for _ in range(self.population_size):
            random.shuffle(arrangement)
            print("Creating permutation", arrangement)
            permutation = Permutation(self.population_size, arrangement)
            self.fitness(permutation)
            self.permutations.append(permutation)

    def total_fitness(self):
        """Returns the total fitness of all permutations"""
        return sum([permutation.fitness for permutation in self.permutations])

    def apply_roulette_selection(self):
        """Apply fi/favg to get roulette"""
        roulette = []
        generation_size = len(self.permutations)
        for perm in self.permutations:
            avg_fitness = self.total_fitness() / generation_size
            roulette += [perm] * int((perm.fitness / avg_fitness)) if avg_fitness > 0 else []
        self.permutations = roulette

    def apply_crossover(self):
        """Take 2 random mates, select random crossover point. Produce two offsprings"""
        crossed_over = []
        generation_size = len(self.permutations)
        for _ in range(generation_size // 2):
            crossover_point = random.randint(0, self.population_size - 1)
            parent_one = self.permutations[random.randint(0, generation_size - 1)]
            parent_two = self.permutations[random.randint(0, generation_size - 1)]

            crossed_over.append(Permutation(generation_size,
                                            parent_one.arrangement[:crossover_point] +
                                            parent_two.arrangement[crossover_point:]))
            crossed_over.append(Permutation(generation_size,
                                            parent_two.arrangement[:crossover_point] +
                                            parent_one.arrangement[crossover_point:]))
        self.permutations = crossed_over

    def apply_mutation(self, rate: float):
        """Change the queens of permutation based on probabilistic rate"""
        for permutation in self.permutations:
            for index in self.board:
                if random.random() > rate:
                    permutation.arrangement[index] = random.randint(0, self.population_size - 1)

    def fitness(self, permutation: Permutation):
        """permutation is one Permutation with length = self.population_size"""
        for row in self.board:
            queen_col = permutation.arrangement[row]
            # count queens in the same col
            permutation.fitness += permutation.arrangement.count(queen_col) - 1
            # count queens in the same row
            permutation.fitness += permutation.arrangement.count(row) - 1

            # check the four diagnols
            for i in range(0, self.population_size):
                _up = row - i
                down = row + i
                right = queen_col + i
                left = queen_col - i

                if (_up == row or down == row) and (right == queen_col or left == queen_col):
                    # don't count the queen we are currently checking
                    continue

                if _up >= 0:
                    queen = permutation.arrangement[_up]
                    if queen == left or queen == right:
                        permutation.fitness += 1
                if down < self.population_size:
                    queen = permutation.arrangement[down]
                    if queen == left or queen == right:
                        permutation.fitness += 1

            if permutation.fitness == 0:
                raise GoalFound("Goal with fitness", permutation.fitness, permutation.arrangement)

            return permutation.fitness

    def generate(self, count: int, mutation_rate: float):
        """Apply roulette, crossover, and mutations count times with rate"""
        for _ in range(count):
            self.total_fitness()
            self.apply_roulette_selection()
            print("Applied roulette", len(self.permutations))
            self.apply_crossover()
            print("Applied crossover", len(self.permutations))
            self.apply_mutation(mutation_rate)
            print("Applied mutation", len(self.permutations))


if __name__ == '__main__':
    ga = GeneticAlgorithm(4)
    print("before generate fitness: ", ga.total_fitness())
    ga.generate(10, 0.001)
    print("after generate fitness: ", ga.total_fitness())

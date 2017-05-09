import itertools


class Permutation(object):
    def __init__(self, N: int, arrangement: list, fitness: int=0):
        self.population_size = N
        self.fitness = fitness or 0
        self.arrangement = arrangement


class GeneticAlgorithm(object):
    """index: row, value: row"""
    def __init__(self, N: int):
        self.population_size = N
        self.board = list(range(self.population_size))
        total_fitness = 0

        self.permutations = []
        for permutation in itertools.permutations(range(self.population_size)):
            fitness = self.fitness(permutation)
            total_fitness += fitness
            self.permutations.append(Permutation(self.population_size, permutation, fitness))

        self.avg_fitness = float(total_fitness) / self.population_size

    def apply_roulette_selection(self):
        """Apply fi/favg to roulette"""
        roulette = []
        for permutation in self.permutations:
            roulette += [permutation] * (permutation.fitness / self.avg_fitness)
        return roulette

    def apply_crossover(self):
        pass

    def apply_mutation(self):
        pass

    def fitness(self, permutation: Permutation):
        """permutation is one Permutation with length = self.population_size"""
        for row in self.board:
            queen_col = permutation.arrangement[row]
            print('row', row, 'col', queen_col)
            # count queens in the same col
            permutation.fitness += permutation.arrangement.count(queen_col) - 1
            # count queens in the same row
            permutation.fitness += permutation.arrangement.count(row) - 1

            print("perm before diagnols", permutation.fitness)
            # check the four diagnols
            for i in range(0, self.population_size):
                up = row - i
                down = row + i
                right = queen_col + i
                left = queen_col - i

                if (up == row or down == row) and (right == queen_col or left == queen_col):
                    # don't count the queen we are currently checking
                    continue

                if up >= 0:
                    queen = permutation.arrangement[up]
                    if queen == left or queen == right:
                        permutation.fitness += 1
                if down < self.population_size:
                    queen = permutation.arrangement[down]
                    if queen == left or queen == right:
                        permutation.fitness += 1
            print("perm fitness", permutation.fitness)

if __name__ == '__main__':
    n = 4
    ga = GeneticAlgorithm(n)
    perm = Permutation(n, [3, 1, 0, 2])
    print(perm.arrangement)
    ga.fitness(perm)
    print("total", perm.fitness)

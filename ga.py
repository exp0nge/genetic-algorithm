import itertools


class Permutation(object):
    def __init__(self, N: int, arrangement: list):
        self.population_size = N
        self.score = 0
        self.arrangement = arrangement


class GeneticAlgorithm(object):
    """index: row, value: row"""
    def __init__(self, N: int):
        self.population_size = N
        self.permutations = list(itertools.permutations(range(self.population_size)))
        self.board = list(range(self.population_size))

    def apply_roulette_selection(self):
        pass

    def apply_crossover(self):
        pass

    def apply_mutation(self):
        pass

    def fitness(self, permutation: Permutation):
        """permutation is one permutation"""
        for row in self.board:
            queen_col = permutation.arrangement[row]
            print('row', row,'col', queen_col)
            # count queens in the same col
            permutation.score += permutation.arrangement.count(queen_col) - 1
            # count queens in the same row
            permutation.score += permutation.arrangement.count(row) - 1

            # check the four diagnols
            for i in range(row, self.population_size):
                for j in range(queen_col, self.population_size):
                    # + i, + j -> up, right
                    up = row - j
                    down = row + i
                    right = queen_col + j
                    left = queen_col - j
                    if up >= 0 and up != row:
                        queen = permutation.arrangement[up]
                        if queen == left or queen == right:
                            permutation.score += 1
                    if down < self.population_size and down != row:
                        queen = permutation.arrangement[down]
                        if queen == left or queen == right:
                            permutation.score += 1
                print(permutation.score)

if __name__ == '__main__':
    n = 4
    ga = GeneticAlgorithm(n)
    perm = Permutation(n, list(range(n)))
    print(perm.arrangement)
    ga.fitness(perm)
    print("total", perm.score)

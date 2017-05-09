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
        """permutation is one Permutation with length = self.population_size"""
        for row in self.board:
            queen_col = permutation.arrangement[row]
            print('row', row, 'col', queen_col)
            # count queens in the same col
            permutation.score += permutation.arrangement.count(queen_col) - 1
            # count queens in the same row
            permutation.score += permutation.arrangement.count(row) - 1

            print("perm before diagnols", permutation.score)
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
                        permutation.score += 1
                if down < self.population_size:
                    queen = permutation.arrangement[down]
                    if queen == left or queen == right:
                        permutation.score += 1
            print("perm score", permutation.score)

if __name__ == '__main__':
    n = 4
    ga = GeneticAlgorithm(n)
    perm = Permutation(n, [3, 1, 0, 2])
    print(perm.arrangement)
    ga.fitness(perm)
    print("total", perm.score)

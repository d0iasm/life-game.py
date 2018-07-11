import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


CELLS_WIDTH = 7

class LifeGame(object):
    def __init__(self, cells):
        self.cells = np.copy(cells)
        self.shape = cells.shape
        print("SHAPE: ", self.shape)
        # print("SLICED: ")
        # print(self.slice_surrounding_cells(cells, 3, 2))
        print("COUNT: ", self.count_alive(cells, 2, 2))
        # print("NEXT STEP: ", self.one_step())

    def slice_surrounding_cells(self, cells, x, y):
        return cells[y-1:y+2, x-1:x+2]

    def count_alive(self, cells, x, y):
        return np.count_nonzero(
            self.slice_surrounding_cells(cells, x, y)) - cells[y][x]

    def rule(self, cells, x, y):
        count = self.count_alive(cells, x, y)
        is_alive = cells[y][x]
        if count == 3:
            # print("COUNT3! x, y, sliced: ", x, y)
            # print(self.slice_surrounding_cells(cells, x, y))
            return 1
        elif is_alive == 1 and count == 2:
            # print("COUNT2! x, y, sliced: ", x, y)
            # print(self.slice_surrounding_cells(cells, x, y))
            return 1
        else:
            return 0

    def one_step(self):
        cells_next = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'int')
        for j in range(CELLS_WIDTH):
            for i in range(CELLS_WIDTH):
                cells_next[i][j] = self.rule(self.cells, i, j)
        return cells_next

    def play(self, steps = 100):
        for i in range(steps):
            self.cells = self.one_step()
            print("i and current cells: ", i)
            print(self.cells)
        return self.cells


if __name__ == '__main__':
    # cells = np.arange(49).reshape(CELLS_WIDTH, CELLS_WIDTH)
    cells = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'int')
    cells[CELLS_WIDTH//2, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 1
    cells[CELLS_WIDTH//2+1, CELLS_WIDTH//2] = 1
    print(cells)

    lg = LifeGame(cells)
    print(lg.play()) 

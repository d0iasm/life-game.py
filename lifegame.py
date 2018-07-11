import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

CELLS_WIDTH = 7


class LifeGame(object):
    def __init__(self, cells):
        self.cells_prev = np.copy(cells)
        self.cells_next = np.copy(cells)
        self.shape = cells.shape
        print("SHAPE: ", self.shape)
        print("SLICED: ")
        print(self.slice_surrounding_cells(cells, 2, 2))
        print("COUNT: ", self.count_alive(2, 2))

    def slice_surrounding_cells(self, cells, x, y):
        return cells[y-1:y+2, x-1:x+2]

    def count_alive(self, x, y):
        return np.count_nonzero(self.slice_surrounding_cells(self.cells_prev, x, y)) - self.cells_prev[y][x]

if __name__ == '__main__':
    # cells = np.arange(49).reshape(CELLS_WIDTH, CELLS_WIDTH)
    cells = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'int')
    cells[CELLS_WIDTH//2, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 1
    cells[CELLS_WIDTH//2+1, CELLS_WIDTH//2] = 1
    print(cells)

    lg = LifeGame(cells)


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class LifeGame(object):
    def __init__(self, cells):
        self.cells = np.copy(cells)

    def slice_surrounding_cells(self, cells, x, y):
        return cells[max(y-1, 0):y+2, max(x-1, 0):x+2]

    def count_alive(self, cells, x, y):
        return np.count_nonzero(
            self.slice_surrounding_cells(cells, x, y)) - cells[y][x]

    def rule(self, cells, x, y):
        count = self.count_alive(cells, x, y)
        is_alive = cells[y][x]
        if count == 3 or (is_alive == 1 and count == 2):
            return 1
        else:
            return 0

    def one_step(self):
        cells_next = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'int')
        for j in range(CELLS_WIDTH):
            for i in range(CELLS_WIDTH):
                cells_next[i][j] = self.rule(self.cells, i, j)
        return cells_next

    def play(self, steps = 200):
        for i in range(steps):
            self.cells = self.one_step()
            print("i and current cells: ", i)
            print(self.cells)
        return self.cells

    def one_plt(self):
        cells_next = self.one_step()
        self.cells = cells_next
        print(cells_next)
        plt.pcolor(cells_next)
        plt.colorbar()


FIG = plt.figure()

CELLS_WIDTH = 11
INIT_CELLS = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'int')
INIT_CELLS[CELLS_WIDTH//2, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 1
INIT_CELLS[CELLS_WIDTH//2+1, CELLS_WIDTH//2] = 1
LG = LifeGame(INIT_CELLS)

def update(t):
    print("COUNT: ", t);
    FIG.clear()
    LG.one_plt()

def plt_anime(ival = 25):
    ani = animation.FuncAnimation(FIG, update, interval=ival, repeat=False)
    plt.show()

if __name__ == '__main__':
    plt_anime(50)

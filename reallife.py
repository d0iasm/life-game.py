import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class LifeGame(object):
    def __init__(self, cells):
        self.cells = np.copy(cells)

    def slice_surrounding_cells(self, cells, x, y):
        return cells[max(y-1, 0):y+2, max(x-1, 0):x+2]

    def rule(self, cells, x, y):
        s = np.sum(self.slice_surrounding_cells(cells, x, y))
        if TL <= s - cells[y][x] <= TH:
            return True, self.increase(cells, x, y)
        else:
            return False, self.decrease(cells, x, y)

    def increase(self, cells, x, y):
        return 1 - (1 - cells[y][x]) / F

    def decrease(self, cells, x, y):
        return cells[y][x] / F

    def one_step(self):
        cells_next = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'float')
        for j in range(CELLS_WIDTH):
            for i in range(CELLS_WIDTH):
                is_increase, d = self.rule(self.cells, i, j)
                if is_increase:
                    cells_next[i][j] += d
                else:
                    cells_next[i][j] -= d
        return cells_next

    def play(self, steps = 200):
        for i in range(steps):
            self.cells = self.one_step()
            print("COUNT: ", i)
            # print(self.cells)
        return self.cells

    def one_plt(self):
        cells_next = self.one_step()
        self.cells = cells_next
        print(cells_next)
        plt.pcolor(cells_next, vmin=0.0, vmax=1.0)
        plt.colorbar()


FIG = plt.figure()

CELLS_WIDTH = 100
INIT_CELLS = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'float')
INIT_CELLS[CELLS_WIDTH//2, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 0.5
# INIT_CELLS[CELLS_WIDTH//2-CELLS_WIDTH//4, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 0.5
# INIT_CELLS[CELLS_WIDTH//2+CELLS_WIDTH//4, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 0.5
LG = LifeGame(INIT_CELLS)

## Art version.1
# TL = 1.0
# TH = 5.0
# F = 2.0

## Art version.2
TL = 0.01 
TH = 2.0
F = 1.1


def update(t):
    print("COUNT: ", t);
    FIG.clear()
    LG.one_plt()

def plt_anime(ival = 25, save_file = False):
    ani = animation.FuncAnimation(FIG, update, interval=ival, repeat=False)
    plt.show()
    # if save_file: ani.save(save_file, writer='imagemagick')

if __name__ == '__main__':
    plt_anime(10)

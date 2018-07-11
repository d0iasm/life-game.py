import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MultipleLocator


class LifeGame(object):
    STATE = {'alive': 2, 'death': 0, 'birth': 1}

    def __init__(self, cells):
        self._cells_initial = np.copy(cells) # 初期のセル配列
        self._cells_in = np.copy(cells) # ルール適用前のセル配列
        self._cells_out = np.copy(cells) # ルール適用後のセル配列 np.copy(cells)
        self._SHAPE = cells.shape

    def get_shape(self):
        return self._SHAPE

    def _isAlive(self, cell_idx):
        '''
        check if the cell of idx is alive. 
        '''
        if self._cells_in[cell_idx] == self.STATE['death']:
            return False
        return True

    def _count_alive_surrounding(self, cell_idx):
        '''
        count alive cells in surrounding 8 cells

        Return:
        int
        note:自分のセル分も含まれる
        '''  
        range_idx = [(idx - 1 if idx - 1 >= 0 else 0, idx + 2 if idx + 2 <= maximum else maximum) for idx, maximum in zip(cell_idx, self._SHAPE)]
        #print(cell_idx, range_idx, np.count_nonzero(self._cells_in[range_idx[0][0]:range_idx[0][1], range_idx[1][0]:range_idx[1][1]]))
        return np.count_nonzero(self._cells_in[range_idx[0][0]:range_idx[0][1], range_idx[1][0]:range_idx[1][1]])


    def rule_alive_condition_setting(min_cell_num:int, max_cell_num:int):

        def _rule_alive_condition(self, cell_idx):
            if self._isAlive(cell_idx) and (min_cell_num <= self._count_alive_surrounding(cell_idx) - 1 <= max_cell_num):
                return True
            return False
        return _rule_alive_condition

    def _rule_alive_apply(self, cell_idx):
        # そのcellはそのまま生存　なにもしない
        self._cells_out[cell_idx] = self.STATE['alive']


    def rule_birth_condition_setting(birth_required_cell_num:int):
        
        def _rule_birth_condition(self, cell_idx):
            # 周囲8マス以内に他のセルがbirth_required_cell_numだけ生きていれば
            if not self._isAlive(cell_idx) and (self._count_alive_surrounding(cell_idx) == birth_required_cell_num):
                return True
            return False

        return _rule_birth_condition   

    def _rule_birth_apply(self, cell_idx):
        ## そのcellに誕生
        self._cells_out[cell_idx] = self.STATE['birth']


    def _default_condition(self, cell_idx):
        return True

    def _rule_death_apply(self, cell_idx):
        self._cells_out[cell_idx] = self.STATE['death']

    # Rule
    rules = (
        (rule_alive_condition_setting(2, 3), _rule_alive_apply), # alive
        (rule_birth_condition_setting(3), _rule_birth_apply), # birth
        (_default_condition, _rule_death_apply) # death
    )

    def play(self, count=1):
        '''
        run recursively
        '''
        if count <= 0:
            return self._cells_out

        # copy先のcell
        self._cells_out = np.copy(self._cells_in)
        # index の取得  
        for idx in np.ndindex(self._SHAPE):
            for condition, apply in self.rules:
                if condition(idx, self._cells_in):
                    apply(idx, self._cells_out)
                    break

        print(self._cells_out)
        return play(count-1)

    def _count(self, i):
        x = [i]
        def countup():
            x[0] += 1
            return x[0]
        return countup


    def __iter__(self):
        '''

        '''
        self._cells_in = np.copy(self._cells_initial)
        self._cells_out = np.copy(self._cells_initial)
        self._countup = self._count(0)
        return self

    def __next__(self):
        self._cells_in = np.copy(self._cells_out)
        #index の取得  
        for idx in np.ndindex(self._SHAPE):
            for condition, apply in self.rules:
                if condition(self, idx):
                    apply(self, idx)
                    break

        return self._countup(), self._cells_out

    def __str__(self):
        return self._cells_out.__str__()

    def plt(self, save_file=False):
        fig, ax = plt.subplots()
        plt.axis('scaled') 
        Locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(Locator)
        ax.yaxis.set_major_locator(Locator)

        plt.xlim(0, self._SHAPE[1])
        plt.ylim(self._SHAPE[0], 0)

        rows = np.arange(self._SHAPE[1] + 1)
        cols = np.arange(self._SHAPE[0] +1)
        X, Y = np.meshgrid(rows, cols)

        plt.pcolor(X, Y, self._cells_out, cmap=plt.cm.gray_r)
        plt.grid(True, which='both', axis='both', linestyle='-', color='k')
        plt.show()
        if(save_file):
            plt.savefig(save_file)

    def plt_anime(self, iterate_num=5, interval=700, repeat=True, repeat_delay=500, save_file=False):
        fig, ax = plt.subplots()
        plt.axis('scaled') 
        Locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(Locator)
        ax.yaxis.set_major_locator(Locator)

        plt.xlim(0, self._SHAPE[1])
        plt.ylim(self._SHAPE[0], 0)

        rows = np.arange(self._SHAPE[1] + 1)
        cols = np.arange(self._SHAPE[0] + 1)
        X, Y = np.meshgrid(cols, rows)

        self.__iter__()
        ims = []
        im = plt.pcolor(X, Y, self._cells_out, cmap=plt.cm.gray_r)
        plt.grid(True, which='both', axis='both', linestyle='-', color='k')
        ims.append([im])
        for i in range(iterate_num):
            self.__next__()
            im = plt.pcolor(X, Y, self._cells_out, cmap=plt.cm.gray_r)
            plt.grid(True, which='both', axis='both', linestyle='-', color='k')
            ims.append([im])

        ani = animation.ArtistAnimation(fig, ims, blit=True, interval=interval, repeat=repeat, repeat_delay=repeat_delay)
        if(save_file):
            ani.save(save_file, writer='imagemagick')
        return ani


if __name__ == '__main__':
    CELLS_WIDTH = 30
    cells = np.zeros((CELLS_WIDTH, CELLS_WIDTH), 'int')
    cells[CELLS_WIDTH//2, (CELLS_WIDTH//2-1):(CELLS_WIDTH//2+2)] = 1
    cells[CELLS_WIDTH//2+1, CELLS_WIDTH//2] = 1
    print(cells)

    lg = LifeGame(cells)
    lg.plt_anime(20, save_file='t-tetoromino.gif')

    lg.plt()



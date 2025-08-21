import copy
import numpy as np

class StateTable:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.table = np.zeros((rows, columns))

    def activate(self, row, column):
        self.table[row][column] = 1

    def deactivate(self, row, column):
        self.table[row][column] = 0

    def get_row_column(self):
        return self.rows, self.columns

    def get_cell_state(self, row, column):
        return self.table[row][column]

    def reset(self):
        self.table = np.zeros((self.rows, self.columns))
    def update(self):
        live_cells = np.where(self.table == 1)
        new_table = copy.deepcopy(self.table)
        for row, column in zip(live_cells[0], live_cells[1]):
            neighbors = self.get_live_neighbors(row, column)
            if neighbors < 2 or neighbors > 3:
                new_table[row, column] = 0
            if neighbors == 2 or neighbors == 3:
                new_table[row, column] = 1
        dead_cells = np.where(self.table == 0)
        for row, column in zip(dead_cells[0], dead_cells[1]):
            neighbors = self.get_live_neighbors(row, column)
            if neighbors == 3:
                new_table[row, column] = 1
        self.table = new_table

    def get_live_neighbors(self, row, column):
        neighbors = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                if 0 <= row + i < self.rows and 0 <= column + j < self.columns:
                    neighbors += self.table[row + i][column + j]
        return neighbors


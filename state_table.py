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
        if row == 0 and column == 0:
            neighbors += self.table[row + 1, column]
            neighbors += self.table[row, column + 1]
            neighbors += self.table[row + 1, column + 1]
        elif row == 0 and column == self.columns - 1:
            neighbors += self.table[row + 1, column]
            neighbors += self.table[row, column - 1]
            neighbors += self.table[row + 1, column - 1]
        elif row == self.rows - 1 and column == 0:
            neighbors += self.table[row - 1, column]
            neighbors += self.table[row, column + 1]
            neighbors += self.table[row - 1, column + 1]
        elif row == self.rows - 1 and column == self.columns - 1:
            neighbors += self.table[row - 1, column]
            neighbors += self.table[row, column - 1]
            neighbors += self.table[row - 1, column - 1]
        elif row == 0:
            neighbors += self.table[row + 1, column]
            neighbors += self.table[row, column + 1]
            neighbors += self.table[row + 1, column + 1]
            neighbors += self.table[row, column - 1]
            neighbors += self.table[row + 1, column - 1]
        elif row == self.rows - 1:
            neighbors += self.table[row - 1, column]
            neighbors += self.table[row, column + 1]
            neighbors += self.table[row - 1, column + 1]
            neighbors += self.table[row, column - 1]
        elif column == 0:
            neighbors += self.table[row + 1, column]
            neighbors += self.table[row - 1, column]
            neighbors += self.table[row + 1, column + 1]
            neighbors += self.table[row - 1, column + 1]
            neighbors += self.table[row, column + 1]
        elif column == self.columns - 1:
            neighbors += self.table[row + 1, column]
            neighbors += self.table[row - 1, column]
            neighbors += self.table[row + 1, column - 1]
            neighbors += self.table[row - 1, column - 1]
            neighbors += self.table[row, column - 1]
        else:
            neighbors += self.table[row + 1, column]
            neighbors += self.table[row - 1, column]
            neighbors += self.table[row, column + 1]
            neighbors += self.table[row, column - 1]
            neighbors += self.table[row + 1, column + 1]
            neighbors += self.table[row - 1, column + 1]
            neighbors += self.table[row + 1, column - 1]
            neighbors += self.table[row - 1, column - 1]
        return neighbors


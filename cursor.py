class Cursor:
    def __init__(self, boundaries, row=0, col=0):
        self._row = row
        self._col = col
        self.rows, self.cols = boundaries
        self.col_memory = 0

    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    def pos(self):
        return (self._row, self._col)
    
    def up(self, row_len, from_blank_line=False):
        if self._row > 0:
            self._row -= 1

            if from_blank_line:
                self._col = self.col_memory = row_len
            else:
                self._col = min(row_len, self.col_memory)

    def down(self, row_len, lines):
        if self._row >= self.rows - 1 or self._row >= lines - 1:
            return

        self._row += 1
        self._col = min(row_len, self.col_memory)

    def left(self):
        if self._col > 0:
            self._col -= 1
            self.col_memory = self._col

    def right(self, row_len):
        if self._col >= self.cols - 1 or self._col >= row_len:
            return
        
        self._col += 1
        self.col_memory = self._col

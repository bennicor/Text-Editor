class Cursor:
    def __init__(self, boundaries, row=0, col=0, rows_before_scroll=0):
        self._row = row
        self._col = col
        self.window_height, self.window_width = boundaries
        self.col_memory = 0
        self._scroll_offset = 0
        self._rows_before_scroll = rows_before_scroll

    @property
    def row(self):
        return self._row
    
    @property
    def col(self):
        return self._col
    
    @property
    def scroll_offset(self):
        return self._scroll_offset
    
    def pos(self):
        return (self._row, self._col)
    
    def up(self, prev_row_len, from_removed_line=False):
        if self._row > self._rows_before_scroll:
            self._row -= 1
        elif self._scroll_offset > 0:
            self._scroll_offset -= 1
        elif self._row > 0 and self.scroll_offset == 0:
            self._row -= 1

        if from_removed_line:
            self._col = self.col_memory = prev_row_len
        else:
            self._col = min(prev_row_len, self.col_memory)

    def down(self, next_row_len, total_lines, new_line=False):
        inside_window = self._row < self.window_height - self._rows_before_scroll - 1
        inside_lines_limit = self._row + self._scroll_offset < total_lines - 1

        if inside_window and inside_lines_limit:
            self._row += 1
        elif inside_lines_limit:
            self._scroll_offset += 1

        if new_line:
            self._col = self.col_memory = next_row_len
        else:
            self._col = min(next_row_len, self.col_memory)

    def left(self):
        if self._col > 0:
            self._col -= 1
            self.col_memory = self._col

    def right(self, row_len):
        if self._col < row_len and self._col < self.window_width - 1:
            self._col += 1
            self.col_memory = self._col

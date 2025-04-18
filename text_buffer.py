class TextBuffer:
    def __init__(self):
        self.text = [""]
        self._lines = len(self.text)

    @property
    def lines(self):
        return self._lines
    
    def get_row(self, index):
        if 0 <= index < len(self.text):
            return self.text[index]
        return []
    
    def new_line(self, row, col):
        line = self.text[row]
        self.text[row] = line[:col]
        self.text.insert(row + 1, line[col:])
        self._lines += 1

    def insert(self, row, col, char):
        if not (0 <= row < self._lines):
            return
        
        line = self.text[row]
        self.text[row] = line[:col] + char + line[col:]

    def backspace(self, row, col):
        if not (0 <= row < self._lines):
            return 0

        current_line = self.text[row]
        if col == 0 and row > 0:
            prev_line = self.text[row - 1]

            self.text[row - 1] = prev_line + current_line
            self.text.pop(row)
            self._lines -= 1

            return len(prev_line)

        if col > 0:
            self.text[row] = current_line[:col - 1] + current_line[col:]
            return col - 1

        return col

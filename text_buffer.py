class TextBuffer:
    def __init__(self):
        self.text = [[]]
        self._lines = len(self.text)

    @property
    def lines(self):
        return self._lines
    
    def get_row(self, index):
        if 0 <= index < len(self.text):
            return self.text[index]
        return []
    
    def new_line(self, row):
        self.text.insert(row, [])
        self._lines += 1

    def insert(self, row, col, char):
        if not (0 <= row < self._lines):
            return
        
        self.text[row].insert(col, char)

    def backspace(self, row, col):
        if col < 0:
            return
        
        if len(self.text[row]) == 0:
            if self._lines == 1 or row == 0:
                return
            
            self.text.pop(row)
            self._lines -= 1
        else:
            self.text[row].pop(col)

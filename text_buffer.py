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
        self.text[row].insert(col, char)

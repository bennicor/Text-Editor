class TextBuffer:
    def __init__(self):
        self.text = [[]]

    def get_row(self, index):
        if 0 <= index < len(self.text):
            return self.text[index]
    
    def new_line(self):
        self.text.append([])

    def insert(self, row, col, char):
        self.text[row].insert(col, char)

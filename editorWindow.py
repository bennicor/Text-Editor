from text_buffer import TextBuffer
from cursor import Cursor
from curses import keyname


class EditorWindow:
    def __init__(self, window):
        self.window = window
        self.buffer = TextBuffer()
        self.cursor = Cursor(window.getmaxyx())
        
        self.prev_line = ""
        self.cur_line = ""
        self.next_line = ""

    def start(self):
        y, x = self.cursor.pos()

        while True:
            self.prev_line = self.buffer.get_row(y - 1)
            self.cur_line = self.buffer.get_row(y)
            self.next_line = self.buffer.get_row(y + 1)

            key = self.window.getch()
            k = keyname(key).decode()

            if k == "KEY_UP":
                self.cursor.up(len(self.prev_line))
            elif k in ("KEY_DOWN"):
                self.cursor.down(len(self.next_line), self.buffer.lines)
            elif k in ("KEY_ENTER", "^J"):
                self.new_line(y)
            elif k == "KEY_LEFT":
                self.cursor.left()
            elif k == "KEY_RIGHT":
                self.cursor.right(len(self.cur_line))
            elif k in ("KEY_BACKSPACE", "^H"):
                pass
            else:
                if len(k) > 1:
                    continue

                self.insert(y, x, k)

            y, x = self.cursor.pos()
            self.window.move(y, x)

            self.window.refresh()

    def insert(self, row, col, char):
        self.buffer.insert(row, col, char)
        
        self.window.move(row, 0)
        self.window.clrtoeol()
        self.cursor.right(len(self.cur_line))

        line = self.buffer.get_row(row)
        self.window.addstr(row, 0, "".join(line))
    
    def new_line(self, row):
        self.buffer.new_line(row + 1)

        for i in range(row + 1, self.buffer.lines):
            self.window.move(i, 0)
            self.window.clrtoeol()
            
            line = self.buffer.get_row(i)
            self.window.addstr(i, 0, "".join(line))

        self.cursor.down(len(self.buffer.get_row(row + 1)), self.buffer.lines)

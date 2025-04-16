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
        self.main_loop(y, x)

    def main_loop(self, y, x):
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
                self.buffer.new_line(y + 1)
                self.lines_render(y)
                self.cursor.down(0, self.buffer.lines)
            elif k == "KEY_LEFT":
                self.cursor.left()
            elif k == "KEY_RIGHT":
                self.cursor.right(len(self.cur_line))
            elif k in ("KEY_BACKSPACE", "^H"):
                self.backspace(y, x)
            else:
                if len(k) > 1:
                    continue
                
                self.buffer.insert(y, x, k)
                self.line_render(y)
                self.cursor.right(len(self.cur_line))

            y, x = self.cursor.pos()
            self.window.addstr(10, 0, f"{y} {x} {self.cursor.col_memory}")
            self.window.move(y, x)

            self.window.refresh()

    def line_render(self, row):
        self.window.move(row, 0)
        self.window.clrtoeol()

        line = self.buffer.get_row(row)
        self.window.addstr(row, 0, "".join(line))
    
    def lines_render(self, row):
        self.window.move(row, 0)
        self.window.clrtobot()

        for i in range(row, self.buffer.lines):
            line = self.buffer.get_row(i)
            self.window.addstr(i, 0, "".join(line))

    def backspace(self, row, col):
        if len(self.cur_line) == 0:
            self.buffer.backspace(row, col)
            self.cursor.up(len(self.prev_line), True)
            self.lines_render(row)
        else:
            self.buffer.backspace(row, col - 1)
            self.line_render(row)
            self.cursor.left()

from text_buffer import TextBuffer
from cursor import Cursor
from curses import keyname


class EditorWindow:
    def __init__(self, window):
        self.window = window
        self.buffer = TextBuffer()
        self.cursor = Cursor(window.getmaxyx())

    def start(self):
        y, x = self.cursor.pos()

        while True:
            key = self.window.getch()
            k = keyname(key).decode()

            if k == "KEY_UP":
                row_len = len(self.buffer.get_row(y - 1))
                self.cursor.up(row_len)
            elif k in ("KEY_DOWN", "KEY_ENTER", "^J"):
                self.buffer.new_line()
                row_len = len(self.buffer.get_row(y + 1))
                self.cursor.down(row_len)
            elif k == "KEY_LEFT":
                self.cursor.left()
            elif k == "KEY_RIGHT":
                self.cursor.right()
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
        self.cursor.right()

        line = self.buffer.get_row(row)
        self.window.addstr(row, 0, "".join(line))

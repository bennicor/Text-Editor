from text_buffer import TextBuffer
from cursor import Cursor
import curses


class EditorWindow:
    def __init__(self, window):
        self.window = window
        self.buffer = TextBuffer()
        self.cursor = Cursor(window.getmaxyx())

    def start(self):
        y, x = self.cursor.pos()

        while True:
            key = self.window.getch()
            k = curses.keyname(key).decode()

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
            else:
                if len(k) > 1:
                    continue

                self.window.addch(y, x, k)
                self.buffer.insert(y, k)
                self.cursor.right()

            y, x = self.cursor.pos()
            self.window.move(y, x)

            self.window.refresh()

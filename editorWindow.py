from text_buffer import TextBuffer
from cursor import Cursor
from curses import keyname


class EditorWindow:
    def __init__(self, window):
        self.window = window
        self.window_height, self.window_width = window.getmaxyx()
        self.buffer = TextBuffer()
        self.cursor = Cursor((self.window_height, self.window_width))
        
        self.prev_line = ""
        self.cur_line = ""
        self.next_line = ""

        self.scroll_y = 0

    def load(self):
        with open("./test.txt", "r") as f:
            for i, line in enumerate(f.readlines()):
                line = line.strip()
                for char in range(len(line)):
                    self.buffer.insert(i, char, line[char])
                self.buffer.new_line(i + 1)

    def start(self):
        self.window.clear()
        self.load()
        self.render()

        y, x = 0, 0
        self.window.move(y, x)
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
                
                if self.cursor.scroll_up:
                    new_scroll_y = self.scroll_y - 1

                    if new_scroll_y >= 0:
                        self.scroll_y = new_scroll_y
            elif k in ("KEY_DOWN"):
                self.cursor.down(len(self.next_line), self.buffer.lines)
                
                if self.cursor.scroll_down:
                    delta_scroll_y = self.scroll_y + 1

                    if delta_scroll_y < self.buffer.lines:
                        self.scroll_y = delta_scroll_y
            elif k in ("KEY_ENTER", "^J"):
                self.buffer.new_line(y + 1)
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
                self.cursor.right(len(self.cur_line))

            self.render()

            y, x = self.cursor.pos()
            self.window.move(y, x)
            y += self.scroll_y
            
            self.window.refresh()

    def render(self):
        self.window.clear()

        lines_to_render = min(self.window_height, self.buffer.lines)
        for line_ind in range(lines_to_render):
            row = self.buffer.get_row(line_ind + self.scroll_y)
            self.window.addstr(line_ind, 0, "".join(row))

    def backspace(self, row, col):
        if len(self.cur_line) == 0:
            self.buffer.backspace(row, col)
            self.cursor.up(len(self.prev_line), True)
        else:
            self.buffer.backspace(row, col - 1)
            self.cursor.left()

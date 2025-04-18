import curses
from editorWindow import EditorWindow


def main(stdscr):
    window = EditorWindow(stdscr)
    window.start()


if __name__ == "__main__":
    curses.wrapper(main)
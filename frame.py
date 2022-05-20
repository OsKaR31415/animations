import curses
from typing import TypeVar

# Type to represent a frame modification
# That is a method of *Frame* that modifies the frame
FrameModification = TypeVar('FrameModification')


class Frame:
    def __init__(self, scr) -> None:
        # scr is a curses stdscr
        self.scr = scr

    def put_text(self, y: int, x: int, text: str, col: int =None) -> None:
        if col is None:
            self.scr.addstr(int(y), int(x), str(text))
        else:
            self.scr.addstr(int(y), int(x), str(text), curses.color_pair(col))

    def addstr(self, *args, **kwargs):
        """The original curses function."""
        self.scr.addstr(*args, **kwargs)

    def refresh(self):
        self.scr.refresh()

    def clear(self):
        self.scr.clear()

    def getmaxyx(self):
        """Return a tuple (y, x) of the height and width of the frame."""
        return self.scr.getmaxyx()

    def pause(self):
        # wait for keypress on getkey
        self.scr.nodelay(0)
        # ask for a key
        self.scr.getkey()


    def copy(self):
        return Frame(self.scr)


def main(stdscr):
    frame = Frame(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)



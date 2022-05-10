import curses
from frame import Frame


def initialize_curses_colors():
    curses.start_color()
    curses.use_default_colors()
    # set color_pair for each color
    for i in range(curses.COLORS):
        curses.init_pair(i + 1, i, -1)

def color_test(scr):
    for i in range(255):
        scr.addstr(str(i), curses.color_pair(i))
    scr.getch()



def main(scr):
    initialize_curses_colors()
    color_test(scr)


curses.wrapper(main)


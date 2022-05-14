import curses
from frame import *
from animations import *
from primitives import *


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
    fr = Frame(scr)

    anim = Anim(fr, rainbowed_text(1, 1, "coucou"))

    for modif_list in anim:
        for modif in modif_list:
            modif(fr)
            sleep(0.01)
            fr.refresh()
    fr.pause()


if __name__ == "__main__":
    curses.wrapper(main)



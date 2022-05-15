import curses
from frame import Frame, FrameModification
from animations import Anim, AnimIterator
from primitives import *
from anim_player import play

from random import randint, choice



def initialize_curses_colors():
    """Initialize the color support of curses (256 colors)."""
    curses.curs_set(0)  # hide the cursor
    curses.start_color()
    curses.use_default_colors()
    # set color_pair for each color
    for i in range(curses.COLORS):
        curses.init_pair(i, i, -1)
        # curses.init_pair(i + 256, i,)

def color_test(scr):
    for i in range(255):
        scr.addstr(str(i), curses.color_pair(i))
    scr.getch()


def screen_saver(fr):
    # initilize an empty animation
    anim = Anim(fr, noop)
    # get the screen bounds
    max_y, max_x = fr.getmaxyx()
    for step in range(100):
        x, y = randint(0, max_x-1), randint(0, max_y-2)
        anim <<= Anim(fr, fadeinout(y, x, "•"), step)
    play(fr, anim)

def main(scr):
    initialize_curses_colors()
    fr = Frame(scr)
    screen_saver(fr)
    return

    # fade_in_out = Anim(fr, fadein(5, 5, "coucou")) > Anim(fr, fadeout(5, 5, "coucou"))

    coucou = Anim(fr, fadein(5, 5, "coucou")) >> Anim(fr, fadein(6, 5, "c'est moi"))
    hdyd = Anim(fr, fadein(10, 10, "how do you do ?"))
    anim = coucou > hdyd


    # anim = Anim(fr, addstr(5, 5, "test", curses.color_pair(1)))
    play(fr, anim)



if __name__ == "__main__":
    curses.wrapper(main)



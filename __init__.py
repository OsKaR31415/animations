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

def screen_saver(fr):
    dot1 = Anim(fr, fadeinout(10, 10, "•"))
    dot2 = Anim(fr, fadeinout(10, 11, "•"), after=10)
    dot3 = Anim(fr, fadeinout(10, 12, "•"), after=20)
    dots = dot1 >> dot2 >> dot3
    anim = Wait(fr, dots, 3000)
    play(fr, Anim(frame, anim))

def main(scr):
    initialize_curses_colors()
    fr = Frame(scr)
    screen_saver(fr)

    # fade_in_out = Anim(fr, fadein(5, 5, "coucou")) > Anim(fr, fadeout(5, 5, "coucou"))

    coucou = Anim(fr, fadein(5, 5, "coucou")) >> Anim(fr, fadein(6, 5, "c'est moi"))
    hdyd = Anim(fr, fadein(10, 10, "how do you do ?"))
    well = Anim(fr, fadein(20, 5, "je vais well !"))
    anim = coucou & hdyd & well


    # anim = Anim(fr, addstr(5, 5, "test", curses.color_pair(1)))
    # play(fr, anim)



if __name__ == "__main__":
    curses.wrapper(main)



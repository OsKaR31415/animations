"""
This module contains all the basic animations. They are called primitives.
"""


from animations import *
import curses
from random import randint

# ╺┳╸╻┏┳┓╻┏┓╻┏━╸
#  ┃ ┃┃┃┃┃┃┗┫┃╺┓
#  ╹ ╹╹ ╹╹╹ ╹┗━┛

def Pause(frame):
    """pause and wait for a keypress.
    This returns an Anim object, so Wrapping it with the Anim constructor is
    not required, while it is still possible."""
    return Anim(frame, frame.pause())


def Wait(frame, anim, delay: int =100):
    """Wait for *delay* units."""
    for _ in range(int(delay)):
        yield []
    yield from Anim(frame, anim)(frame)


def Noop(frame):
    yield []


# ┏┓ ┏━┓┏━┓╻┏━╸   ╺┳╸┏━╸╻ ╻╺┳╸
# ┣┻┓┣━┫┗━┓┃┃      ┃ ┣╸ ┏╋┛ ┃
# ┗━┛╹ ╹┗━┛╹┗━╸    ╹ ┗━╸╹ ╹ ╹
# animations that simply show text, with some style

def text(y: int, x: int, string: str, col: int =None):
    """Add the given *string* text at the given x, y coordinates, with the
    given *col* color.
    Args:
        y (int): The line to add the text at.
        x (int): The column to add the text at.
        string (str): The text to add.
        col (int): The color of the text.
    Returns:
        function: The corresponding animation function.
    """
    # closure so ou return a function, not a generator
    def text_generator(frame):
        # second closure so that what is yielded is a function of *frame*.
        yield [lambda frame:
                frame.put_text(int(y), int(x), str(string), int(col))]
    return text_generator


def addstr(*args, **kwargs):
    """Copy of the curses window.addstr function.
    It accepts more parameters than the *text* primitive, so you can have more
    advanced styles, like bold, italics, under line, etc.
    """
    def addstr_generator(frame):
        yield [lambda frame:
                frame.addstr(*args, **kwargs)]
    return addstr_generator

# ⢎⡑ ⡇ ⡷⢾ ⣏⡱ ⡇  ⣏⡉   ⢹⠁ ⣏⡉ ⢇⡸ ⢹⠁   ⢎⡑ ⢹⠁ ⢇⢸ ⡇  ⣏⡉ ⢎⡑
# ⠢⠜ ⠇ ⠇⠸ ⠇  ⠧⠤ ⠧⠤   ⠸  ⠧⠤ ⠇⠸ ⠸    ⠢⠜ ⠸   ⠇ ⠧⠤ ⠧⠤ ⠢⠜

def bold(y: int, x: int, string: str, col: int =None):
    def bold_generator(frame):
        if col is None:
            color = 0
        else:
            color = int(col)
        yield from addstr(int(y), int(x), str(string), curses.A_BOLD + curses.color_pair(color))(frame)
    return bold_generator


def italic(y: int, x: int, string: str):
    def bold_generator(frame):
        if col is None:
            color = 0
        else:
            color = int(col)
        yield from addstr(int(y), int(x), str(string), curses.A_ITALIC + curses.color_pair(color))(frame)


# ⣏⡉ ⣎⣱ ⡏⢱ ⣏⡉   ⣏⡉ ⣏⡉ ⣏⡉ ⣏⡉ ⡎⠑ ⢹⠁ ⢎⡑
# ⠇  ⠇⠸ ⠧⠜ ⠧⠤   ⠧⠤ ⠇  ⠇  ⠧⠤ ⠣⠔ ⠸  ⠢⠜
# effects that only change the color of the same text

def fadein(y: int, x: int, string: str):
    def fadein_generator(frame):
        # yield invisibe at the beginning
        yield from addstr(y, x, string, curses.A_INVIS)(frame)
        for col in range(233, 256):
            yield from text(y, x, string, col)(frame)
    return fadein_generator


def fadeout(y: int, x: int, string: str):
    def fadeout_generator(frame):
        for col in reversed(range(233, 256)):
            yield from text(y, x, string, col)(frame)
        # yield invisible at the end, because 233 is not exactly black
        yield from addstr(y, x, string, curses.A_INVIS)(frame)
    return fadeout_generator


def fadeinout(y: int, x: int, string: str):
    def fadeinout_generator(frame):
        yield from fadein(y, x, string)(frame)
        yield from fadeout(y, x, string)(frame)
    return fadeinout_generator


def color_ramp(y: int, x: int, string: str, col_ramp: list[int]):
    """Show a string with its colors following the given *col_ramp*.
    Can be used to make color effects like random colors, fade int..."""
    def color_ramp_generator(frame):
        for col in col_ramp:
            yield from text(y, x, string, col)(frame)
    return color_ramp_generator


# ╻ ╻╻┏━╸╻ ╻┏━╸┏━┓   ┏━┓┏━┓╺┳┓┏━╸┏━┓
# ┣━┫┃┃╺┓┣━┫┣╸ ┣┳┛   ┃ ┃┣┳┛ ┃┃┣╸ ┣┳┛
# ╹ ╹╹┗━┛╹ ╹┗━╸╹┗╸   ┗━┛╹┗╸╺┻┛┗━╸╹┗╸
# function to modify animations

def repeat(anim, times: int =-1):
    """Repeat *times* times the animation *anim*.
    Args:
        anim (Anim): The animation to repeat.
        times (int): The number of repetitions. Default to -1 that means
                     endless repetitions (as any negative number).
    Returns:
        function: The animation repeated *times* times.
    """
    def repeat_generator(frame):
        if times < 0:
            while True:
                animation = anim(frame)
                yield from animation
                del animation
        else:
            for _ in range(int(times)):
                animation = Anim(frame, anim)
                yield from (animation & animation)(frame)
                del animation
    return repeat_generator

def Repeat(frame, anim, times: int =-1):
    """Repeat *times* times the animation *anim*.
    Args:
        anim (Anim): The animation to repeat.
        times (int): The number of repetitions. Default to -1 that means
                     endless repetitions (as any negative number).
    Returns:
        function: The animation repeated *times* times.
    """
    return Anim(frame, repeat(anim, times))


def slow(anim, factor: int =2):
    """Slow *factor* times the animation *anim*.
    Args:
        anim (Anim or function): The animation to repeat.
        factor (int): The slowing factor (defaults to 2).
    Returns:
        function: The animation slowed.
    """
    def slow_generator(frame):
        anim_generator = anim(frame)
        while True:
            try:
                step = next(anim_generator)
                for _ in range(factor):
                    yield step
            except StopIteration:
                return
    return slow_generator



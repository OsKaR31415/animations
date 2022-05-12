from typing import TypeVar

# Type to represent a frame modification
# That is a method of *Frame* that modifies the frame
FrameModification = TypeVar('FrameModification')

class Frame:
    def __init__(self, scr) -> None:
        # scr is a curses stdscr
        self.scr = scr

    def put_text(self, y: int, x: int, text: str) -> None:
        pass




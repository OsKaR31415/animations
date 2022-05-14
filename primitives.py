from animations import *

def Pause(frame):
    return Anim(frame, frame.pause())

def text(y: int, x: int, string: str, col: int =None):
    def text_generator(frame):
        yield [lambda f: f.put_text(int(y), int(x), str(string), col)]
    return text_generator

def rainbowed_text(y: int, x: int, string: str):
    def rainbowed_text_generator(frame):
        for col in range(16, 256):
            yield from text(y, x, string, col)(frame)
    return rainbowed_text_generator

def repeat(anim, times: int =-1):
    """Repeat *times* times the animation *anim*.
    Args:
        anim (Anim): The animation to repeat.
        times (int): The number of repetitions. Default to -1 that means
                     endless repetitions (as any negative number).
    """
    if times == 0:
        return anim
    return anim >> repeat(anim, times - 1)



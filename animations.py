"""
Module that defines what is an animation.
It is NOT responsible for defining what is a frame, or what an animation should modify.
It only defines a very general *Anim* object.

"""
from itertools import zip_longest

class Anim:
    def __init__(self, animation, after: int =0) -> None:
        """Initialize the object.
        Args:
            animation (generator): The animation function.
            after (int): The delay before the animation starts.
        """
        if not isinstance(after, int):
            raise TypeError(f"The *after* parameter must be an int, not a {type(after)}")
        if after < 0:
            raise ValueError("The *after* parameter must be positive")
        self.__after__ = int(after)
        self.__anim_function__ = animation

    def __iter__(self):
        return AnimIterator(self)

    def __next__(self) -> list:
        if self.__after__ > 0:
            self.__after__ -= 1
            return []
        for step in self.__anim_function__:
            return step
        while True:
            return []

    def __compose_with__(self, other):
        """Compose with another animation.
        Args:
            other (Anim): The animation to add over the current one.
        Returns:
            generator: The new animation formed with composing *self* and *other*.
        Warning: This method returns a generator, so the >> operator is the
                 preferred method to compose animations, since it returns an
                 Anim object.
        """
        for s, o in zip_longest(self, other):
            yield s + o

    def __rshift__(self, other):
        """The >> operator is used to compose two animations.
        That means playing them at the same time.
        Args:
            other (Anim): The animation to add over the current one.
        Returns:
            Anim: The new animation formed with composing *self* and *other*.
        """
        if not isinstance(other, Anim):
            raise TypeError(f"Cannot compose animation with a different type ({type(other)})")
        return Anim(self.__compose_with__(other))

    def __lshift__(self, other):
        """The << operator is used to compose two animations.
        The only different with >> is that, with <<, *self* has the priority,
        while with >>, *other* is the one that overrides.
        """
        if not isinstance(other, Anim):
            raise TypeError(f"Cannot compose animation with a different type ({type(other)})")
        # it's just like >> but swapped !
        return other >> self


class AnimIterator:
    def __init__(self, anim) -> None:
        """Initialize the object.
        Args:
            anim (Anim): The anim object to make the iterator of.
        """
        self.anim = anim

    def __next__(self):
        return next(self.anim)



if __name__ == "__main__":
    def hello_world():
        yield ["hello,"]
        yield ["world!"]

    def sweet_home():
        while True:
            yield ["home"]
            yield ["sweet"]

    def iota():
        i = 0
        while True:
            i += 1
            yield [str(i)]

    HelloWorld = Anim(hello_world(), after=2)
    SweetHome = Anim(sweet_home(), after=3)
    Iota = Anim(iota())

    anim = Iota >> SweetHome << HelloWorld

    for _ in anim:
        input(repr(_))


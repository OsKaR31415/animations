"""
Module that defines what is an animation.
It is NOT responsible for defining what is a frame, or what an animation should modify.
It only defines a very general *Anim* object.

"""
from typing import Type
from itertools import zip_longest, chain
import curses
from frame import FrameModification

class AnimIterator:
    def __init__(self, anim) -> None:
        """Initialize the object.
        Args:
            anim (Anim): The anim object to make the iterator of.
        """
        self.anim = anim

    def __next__(self):
        return next(self.anim)



class Anim:
    def __init__(self, frame, animation, after: int = 0) -> None:
        """Initialize the object.
        Args:
            animation (generator or Anim): The animation function / Anim object.
            after (int): The delay before the animation starts.
        Raises:
            TypeError: If *after* is not an integer
            ValueError: If *after* is not positive
        Example:
            Note that Anim can be used to copy an animation.
            >>> frame = "foo"
            >>> foo_anim_function = lambda frame: "foo"
            >>> my_anim = Anim(frame, foo_anim_function)  # here we have one animation
            >>> my_anim_copy = Anim(frame, my_anim)  # this is the copy
            >>> my_anim is my_anim_copy
            False
            >>> my_anim.__anim_function__ is my_anim_copy.__anim_function__
            >>> # both share the same animation function, but not the same
            >>> # generator, so they really are independant.
        """
        # the frame of the animation
        self.frame = frame
        # the animation function
        if isinstance(animation, Anim):
            # If *animation* is already an *Anim* objec, then just copy it.
            # It is important here that the generator will be recreated, since
            # this is just the function, not the generator (that is what you
            # get when calling the function), so that when you create two
            # animations with the same function, they do not share the same
            # generator.
            # This means that you may use Anim to actually copy an animation.
            self.__anim_function__ = animation.__anim_function__
        else:
            self.__anim_function__ = animation
        # create the animation generator (animation function once called)
        self.reset_animation()
        # the delay before the animation starts
        if not isinstance(after, int):
            raise TypeError(
                f"The *after* parameter must be an int, not a {type(after)}")
        if after < 0:
            raise ValueError("The *after* parameter must be positive")
        self.__after__ = int(after)

    def reset_animation(self) -> None:
        """Reset the animation. This restart the animation and removes any
        delay that it could have before starting.
        This can used both to initialize the object, in *Anim.__init__*, and to
        reset an animation, since it creates/overrides the
        *Anim.__anim_generator__* attribute.
        """
        self.__anim_generator__ = self.__anim_function__(self.frame)

    def __call__(self, frame):
        """Calling the Anim object is the same as calling its animation function.
        The definition speaks by itself :
        return self.__anim_function__(frame)
        """
        return self.__anim_function__(frame)

    def __iter__(self):
        """Returns the iterable version of an animation.
        Returns:
            AnimIterator: The iterator for an animation.
        """
        return AnimIterator(self)

    def __next__(self) -> list[FrameModification]:
        """Gives the next step of the animation.
        Returns:
            list[FrameModification]: The list of modifications to make to the frame.
        """
        if self.__after__ > 0:
            self.__after__ -= 1
            return []
        try:
            modifications = next(self.__anim_generator__)
            # ensure that the returned value is a list
            if isinstance(modifications, list):
                return modifications
            else:
                return [modifications]
        except StopIteration:
            raise StopIteration

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
        def composed_animation(frame):
            """This is a closure.
            It is used to create a new generator, so the two composed
            generators are stil independant and are not linked with the new one
            composed.
            If you don't take care of that, using the new generator will change
            the two others each time you call next on the composed generator.
            This function is a closure because you want to return a function,
            not a generator (a generator is the function once called).
            """
            for s, o in zip_longest(self, other, fillvalue=[]):
                if not isinstance(s, list):
                    s = [s]
                if not isinstance(o, list):
                    o = [o]
                yield s + o
        return composed_animation

    def __rshift__(self, other):
        """The >> operator is used to compose two animations.
        That means playing them at the same time.
        *other* will be added atop of *self*.
        This operator is called "over".
        Args:
            other (Anim): The animation to add over the current one.
        Returns:
            Anim: The new animation formed with composing *self* and *other*.
        """
        if not isinstance(other, Anim):
            other = Anim(self.frame, other)
        return Anim(self.frame, self.__compose_with__(other))

    def __lshift__(self, other):
        """The << operator is used to compose two animations.
        That means playing them at the same time.
        *other* well be added behind of *self* (at the very behind if *self* is
        already a composed animation).
        This operator is called "under".
        Args:
            other (Anim): The animation to add behind the current one.
        Returns:
            Anim: The new animation formed with composing *self* and *other*.
        """
        if not isinstance(other, Anim):
            other = Anim(self.frame, other)
        # it's just like >> but swapped !
        return other >> self


    def __concatenate_with__(self, other):
        """Return a new animation generator that is *self* then *other* : both
        animations are played, but one by one."""
        def concatenated_animation(frame):
            """This is a closure.
            It is used to create a new generator, so the two concatenated
            generators are stil independent and are not linked with the new one
            created by concatenation.
            If you don't take care of that, using the new generator will change
            the two others each time you call next on the new generator.
            This function is a closure because you want to return a function,
            not a generator (a generator is the function once called).
            """
            self_generator = self(frame)
            other_generator = other(frame)
            yield from self_generator
            yield from other_generator
        return concatenated_animation


    def __and__(self, other):
        """The & operator is used to concatenate two animations.
        That means playing them one at a time.
        This operator is called "and" or "then", because it plays the animation
        *self* then *other*.
        Args:
            other (Anim): The animation to add after the current one.
        Returns:
            Anim: The new animation that is *self* then *other*.
        """
        other = Anim(self.frame, other)
        return Anim(self.frame, self.__concatenate_with__(other))




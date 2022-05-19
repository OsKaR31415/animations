


class Stack:
    """
    >>> S = Stack()
    >>> # test push
    >>> S.push('A')
    >>> S.get_head()
    'A'
    >>> S.push('B')
    >>> S.get_head()
    'B'
    >>> S.push('C')
    >>> S.get_head()
    'C'
    >>> # test delete
    >>> S.delete()
    >>> S.get_head()
    'B'
    >>> # test pop
    >>> S.pop()
    'B'
    >>> S.get_head()
    'A'
    >>> S.pop()
    'A'
    >>> # poping from an empty stack
    >>> S.get_head()
    """

    class StackItem:
        """
        >>> A = StackItem('A', None)
        >>> B = StackItem('B', A)
        >>> B.value
        'B'
        >>> B.get_previous() is A
        True
        """
        def __init__(self, value, previous=None):
            """Initialize a stack item.
            Args:
                value: The value that the item contains.
                previous (StackItem): The previous item in the stack.
            """
            self.value = value
            self.__previous__ = previous

        def get_previous(self):
            """Get the previous item in the stack."""
            return self.__previous__

    def __init__(self):
        """Initialize a stack."""
        self.__head__ = None

    def push(self, value):
        """Push a value onto the stack.
        Args:
            value: The value to push.
        """
        foreign_head = self.__head__
        self.__head__ = self.StackItem(value, previous=self.__head__)

    def get_head(self):
        """Get the head of the stack.
        This does not pop the value from the stack.
        Returns:
            the value that is at the top of the stack.
        Raises:
            IndexError: If you pop from an empty stack.
        """
        if self.__head__ is None:
            raise IndexError("pop from empty stack.")
        return self.__head__.value

    def delete(self):
        """Delete the first item from the stack.
        This does not return the value.
        """
        self.__head__ = self.__head__.get_previous()

    def pop(self):
        """Pop the head of the stack (and return its value).
        """
        head_value = self.__head__.value
        self.__head__ = self.__head__.get_previous()
        return head_value





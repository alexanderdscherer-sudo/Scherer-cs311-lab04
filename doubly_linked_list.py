"""
Lab 4: The Memory Linker -- starter.

Complete DoublyLinkedList below. See the assignment,
Part B, for the full requirements. No node may ever become
unreachable from `head` after any sequence of operations.
"""

from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "prev", "next")

    def __init__(self, value: T) -> None:
        self.value = value
        self.prev: Optional["_Node[T]"] = None
        self.next: Optional["_Node[T]"] = None


class DoublyLinkedList(Generic[T]):
    def __init__(self) -> None:
        self.head: Optional[_Node[T]] = None
        self.tail: Optional[_Node[T]] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert_front(self, value: T) -> None:
        # TODO
        raise NotImplementedError

    def insert_back(self, value: T) -> None:
        # TODO
        raise NotImplementedError

    def delete(self, value: T) -> bool:
        """Remove the first node matching `value`. Return True if removed, False if not found."""
        # TODO
        raise NotImplementedError

    def reverse(self) -> None:
        """Reverse the list in place."""
        # TODO
        raise NotImplementedError

    def insert(self, index: int, value: T) -> None:
        """
        Insert `value` so it becomes the element at `index` (0 through
        len(self), inclusive). Traverse from whichever end is closer to
        `index` to minimize steps.
        """
        # TODO
        raise NotImplementedError

    def delete_at(self, index: int) -> T:
        """Remove and return the value at `index`. Raise IndexError if out of range."""
        # TODO
        raise NotImplementedError

    def __iter__(self) -> Iterator[T]:
        # TODO: front-to-back traversal.
        raise NotImplementedError

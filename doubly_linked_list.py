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
        new_node = _Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._size += 1

    def insert_back(self, value: T) -> None:
        new_node = _Node(value)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def delete(self, value: T) -> bool:
        """Remove the first node matching `value`. Return True if removed, False if not found."""
        current = self.head
        while current is not None:
            if current.value == value:
                self._remove_node(current)
                return True
            current = current.next
        return False

    def reverse(self) -> None:
        """Reverse the list in place."""
        current = self.head
        self.tail = current

        while current is not None:
            # Swap prev and next pointers
            current.prev, current.next = current.next, current.prev
            # Move to the next node (which is now in current.prev after the swap)
            if current.prev is None:
                self.head = current
            current = current.prev

    def insert(self, index: int, value: T) -> None:
        """
        Insert `value` so it becomes the element at `index` (0 through
        len(self), inclusive). Traverse from whichever end is closer to
        `index` to minimize steps.
        """
        if index < 0 or index > self._size:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.insert_front(value)
            return
        if index == self._size:
            self.insert_back(value)
            return

        target = self._get_node_at(index)
        new_node = _Node(value)

        # Place new_node before target
        new_node.prev = target.prev
        new_node.next = target
        if target.prev:
            target.prev.next = new_node
        target.prev = new_node

        self._size += 1

    def delete_at(self, index: int) -> T:
        """Remove and return the value at `index`. Raise IndexError if out of range."""
        if index < 0 or index >= self._size:
            raise IndexError("Index out of bounds")

        target = self._get_node_at(index)
        val = target.value
        self._remove_node(target)
        return val

    def __iter__(self) -> Iterator[T]:
        """Front-to-back traversal."""
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    # --- Helper Methods ---

    def _get_node_at(self, index: int) -> _Node[T]:
        """Helper to find node at `index` using optimal traversal route."""
        if index < self._size // 2:
            # Forward traversal
            current = self.head
            for _ in range(index):
                assert current is not None
                current = current.next
        else:
            # Backward traversal
            current = self.tail
            for _ in range(self._size - 1 - index):
                assert current is not None
                current = current.prev

        assert current is not None
        return current

    def _remove_node(self, node: _Node[T]) -> None:
        """Helper to safely unlink a node and update head/tail."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next  # Removing head

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # Removing tail

        node.next = None
        node.prev = None
        self._size -= 1
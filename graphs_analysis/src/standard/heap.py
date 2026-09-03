from typing import Any, List, Optional, Tuple


class CountingHeap:
    """
    A simple binary min-heap that counts priority comparisons and swaps.
    Each item is assumed to be a tuple where the first element is the priority.

    Attributes
    ----------
    data : List[Tuple[Any, ...]]
        Internal storage for the heap items.
    comparisons : int
        Number of priority (key) comparisons performed.
    swaps : int
        Number of swaps performed during heapify-up and heapify-down.

    Methods
    -------
    push(item: Tuple[Any, ...]) -> None
        Insert an item into the heap.
    pop() -> Optional[Tuple[Any, ...]]
        Remove and return the item with the smallest priority.
    total_work() -> int
        Return the sum of all comparisons and swaps.
    """

    def __init__(self) -> None:
        """Initialize an empty heap and reset counters."""
        self.data = []
        self.comparisons = 0
        self.swaps = 0

    def push(self, item: Tuple[Any, ...]) -> None:
        """
        Insert a new item into the heap, tracking swaps and comparisons.

        Parameters
        ----------
        item : Tuple[Any, ...]
            The item to insert. The first element of the tuple is used as the priority.
        """
        self.data.append(item)
        i = len(self.data) - 1
        while i > 0:
            parent = (i - 1) // 2
            self.comparisons += 1
            if self.data[i][0] < self.data[parent][0]:
                self.data[i], self.data[parent] = self.data[parent], self.data[i]
                self.swaps += 1
                i = parent
            else:
                break

    def pop(self) -> Optional[Tuple[Any, ...]]:
        """
        Remove and return the smallest-priority item from the heap.
        Returns None if the heap is empty. Updates counters.

        Returns
        -------
        Optional[Tuple[Any, ...]]
            The item with the lowest priority, or None if the heap is empty.
        """
        if len(self.data) == 0:
            return None
        self.data[0], self.data[-1] = self.data[-1], self.data[0]
        self.swaps += 1
        item = self.data.pop()
        i = 0
        n = len(self.data)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < n:
                self.comparisons += 1
                if self.data[left][0] < self.data[smallest][0]:
                    smallest = left
            if right < n:
                self.comparisons += 1
                if self.data[right][0] < self.data[smallest][0]:
                    smallest = right
            if smallest == i:
                break
            self.data[i], self.data[smallest] = self.data[smallest], self.data[i]
            self.swaps += 1
            i = smallest
        return item

    def total_work(self) -> int:
        """
        Return the total number of comparisons and swaps performed by the heap.

        Returns
        -------
        int
            The sum of comparisons and swaps.
        """
        return self.comparisons + self.swaps

    def visualize(self) -> None:
        """Print the heap as a tree."""
        if not self.data:
            print("[empty heap]")
            return

        self._print_tree(0, "", True)

    def _print_tree(self, index: int, prefix: str, is_left: bool) -> None:
        """Recursively print the heap tree."""

        if index >= len(self.data):
            return

        right = 2 * index + 2
        left = 2 * index + 1

        # Print right subtree first
        if right < len(self.data):
            self._print_tree(right, prefix + ("│   " if is_left else "    "), False)

        # Print current node
        print(prefix + ("└── " if is_left else "┌── ") + str(self.data[index]))

        # Print left subtree
        if left < len(self.data):
            self._print_tree(left, prefix + ("    " if is_left else "│   "), True)

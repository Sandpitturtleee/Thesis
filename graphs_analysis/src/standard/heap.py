class MinHeap:
    def __init__(self):
        self.heap = []
        self.position = {}
        self.build_count = 0  # number of building (initial pushes)
        self.sift_up_count = 0  # number of sift_ups (includes insert and decrease-key)
        self.sift_down_count = 0  # number of sift_downs
        self.decrease_key_count = 0  # number of decrease_key calls

    def _swap(self, i, j):
        self.position[self.heap[i][1]] = j
        self.position[self.heap[j][1]] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _sift_up(self, idx):
        self.sift_up_count += 1
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx][0] < self.heap[parent][0]:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx):
        self.sift_down_count += 1
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] < self.heap[smallest][0]:
                smallest = right
            if smallest == idx:
                break
            self._swap(idx, smallest)
            idx = smallest

    def push(self, priority, node):
        self.build_count += 1  # Count pushes during build (initial heap)
        self.heap.append((priority, node))
        idx = len(self.heap) - 1
        self.position[node] = idx
        self._sift_up(idx)

    def pop(self):
        if not self.heap:
            raise IndexError("pop from empty heap")
        self._swap(0, len(self.heap) - 1)
        priority, node = self.heap.pop()
        del self.position[node]
        if self.heap:
            self._sift_down(0)
        return priority, node

    def decrease_key(self, node, new_priority):
        self.decrease_key_count += 1
        idx = self.position[node]
        old_priority, _ = self.heap[idx]
        if new_priority < old_priority:
            self.heap[idx] = (new_priority, node)
            self._sift_up(idx)

    def is_empty(self):
        return not self.heap

    def __contains__(self, node):
        return node in self.position

    def stats(self):
        return {
            "build_pushes": self.build_count,
            "sift_up": self.sift_up_count,
            "sift_down": self.sift_down_count,
            "decrease_key": self.decrease_key_count,
            "total": self.build_count
            + self.sift_up_count
            + self.sift_down_count
            + self.decrease_key_count,
        }

    def total(self):
        return (
            self.build_count
            + self.sift_up_count
            + self.sift_down_count
            + self.decrease_key_count
        )

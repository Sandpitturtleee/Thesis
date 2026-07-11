class CountingHeap:
    def __init__(self):
        self.data = []
        self.comparisons = 0
        self.swaps = 0

    def push(self, item):
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

    def pop(self):
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

    def total_work(self):
        return self.comparisons + self.swaps

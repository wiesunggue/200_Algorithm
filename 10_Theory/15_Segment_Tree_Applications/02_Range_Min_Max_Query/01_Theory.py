import sys
sys.setrecursionlimit(10**5)

class MinSegmentTree:
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr
        self.size = 1

        while self.size < self.N:
            self.size *= 2
        
        self.tree = [10**10] * (2 * self.size)
        self._build(1, 0 , self.N - 1)
        
    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.tree[node]
        
        mid = (left + right)//2
        self.tree[node] = min(self._build(node * 2, left, mid), self._build(node * 2 + 1, mid + 1, right))

        return self.tree[node]
    

    def _query(self, node, left, right, l, r):
        if right < l or r < left:
            return 10**10
        
        if l<= left and right<=r:
            return self.tree[node]
        
        mid = (left + right) // 2
        return min(self._query(node * 2, left, mid, l, r), self._query(node*2+1, mid+1, right, l, r))
    
    def _update(self, node, left, right, index, value):
        if left == right:
            self.tree[node] = value
            self.arr[index] = value
            return
        
        mid = (left + right) // 2
        if index<=mid:
            self._update(node * 2, left, mid, index, value)
        else:
            self._update(node * 2 + 1, mid + 1, right, index, value)
        
        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])

    def update(self, index, value):
        self._update(1, 0, self.N-1, index, value)

    def query(self, left, right):
        return self._query(1, 0, self.N-1, left, right)


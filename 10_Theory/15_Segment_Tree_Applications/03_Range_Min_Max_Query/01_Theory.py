import sys
'''Min Max Query의 경우 다음과 같은 연산이 가능하다
1. Max Query + Add Range
2. Max Query + Substitute Range
3. Max Query + 
'''
class RecursiveMaxSegmentTree:
    '''Update는 구간 대입 연산, Query는 구간 내 최댓값 탐색'''
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr
        self.size = 1

        while self.size < self.N:
            self.size *= 2

        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self.haslazy = [False] * (2 * self.size)

        self._build(1, 0, self.N-1)

    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.tree[node]

        mid = (left + right)//2
        self.tree[node] = max(self._build(node*2, left, mid), self._build(node*2+1, mid+1, right))
        return self.tree[node]

    def _push(self,node, left, right):
        if not self.haslazy[node]:
            return

        if left == right:
            return

        value = self.lazy[node]
        mid = (left + right)//2
        self._apply(node*2,left, mid, value)
        self._apply(node*2+1, mid+1, right, value)

        self.lazy[node] = 0
        self.haslazy[node] = False

    def _apply(self,node, left, right, value):
        self.tree[node] = value
        self.haslazy[node] = True
        self.lazy[node] = value

    def update(self, l, r, value):
        self._update(1, 0, self.N-1, l, r, value)

    def _update(self,node,left,right,l,r,value):
        if right < l or r < left:
            return

        if l<=left and right <= r:
            self._apply(node, left, right, value)
            return

        self._push(node, left, right)
        
        mid = (left + right)//2

        self._update(node*2,left,mid,l,r,value)
        self._update(node*2+1,mid+1,right,l,r,value)

        self.tree[node] = max(self.tree[node*2], self.tree[node*2+1])

    def query(self,l,r):
        return self._query(1,0, self.N-1, l, r)

    def _query(self,node, left, right, l, r):
        if right < l or r < left:
            return -10**10

        if l<=left and right <= r:
            return self.tree[node]

        self._push(node, left, right)

        mid = (left + right)//2
        return max(self._query(node*2,left, mid,l,r),self._query(node*2+1,mid+1,right, l,r))
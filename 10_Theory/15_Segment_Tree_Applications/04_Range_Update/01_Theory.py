# Range Segment Tree
'''Range Query의 경우 다음과 같은 연산이 가능하다
1. Max Query + Range Add
2. Max Query + Range Assign
3. Range Sum + Range Assign
4. Range Sum + Range Assign + Range Add
5. Range Sum + Range Multiply
6. Range Sum + Range Affine
7. Range XOR + Range XOR
8. Range Sum + Range XOR
'''
class RecursiveRangeSegmentTree:
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr
        self.size = 1

        while self.size < self.N:
            self.size *= 2

        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self._build(1, 0, self.N-1)

    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.tree[node]

        mid = (left+right)//2
        self.tree[node] = self._build(node * 2, left, mid) + self._build(node*2+1, mid+1, right)

        return self.tree[node]

    def query(self, l, r):
        return self._query(1, 0, self.N-1, l, r)

    def _query(self, node, left, right, l, r):
        if right < l or r < left:
            return 0

        if l<=left and right<=r:
            return self.tree[node]

        # 일부만 겹치는 경우 -> Lazy를 하위로 내려줘야 함
        self._push(node, left, right)
        
        mid = (left+right)//2
        return self._query(node*2, left, mid,l,r) + self._query(node*2+1, mid+1, right, l, r)

    def update(self, l, r, value):
        '''[Left, Right]에 모두 value를 더하는 함수'''
        self._update(1, 0, self.N-1, l,r,value)

    def _update(self, node, left, right, l, r, value):
        if right < l or r < left:
            return

        if l<=left and right<=r:
            self._apply(node,left, right, value)
            return

        self._push(node, left, right)

        mid = (left+right)//2

        self._update(node * 2, left, mid, l, r, value)
        self._update(node * 2 + 1, mid+1, right, l, r, value)

        self.tree[node] = self.tree[node * 2] + self.tree[node*2+1]
        
    def _push(self, node, left, right):
        '''Lazy에 있는 값을 다음 노드에 실제로 넣기'''
        if self.lazy[node] == 0:
            return

        if left == right:
            return

        mid = (left+right)//2
        value = self.lazy[node]

        self._apply(node * 2, left, mid, value)
        self._apply(node * 2 + 1, mid + 1, right, value)

        self.lazy[node] = 0

    def _apply(self, node, left, right, value):
        '''총 합의 연산을 node에서 종료'''
        length = right-left+1
        self.tree[node] += length * value
        self.lazy[node] += value

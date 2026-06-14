import sys
sys.setrecursionlimit(10**5)

# 1. 세그먼트 트리 클래스
class SegmentTree:
    '''구간 합 세그먼트 트리'''
    def __init__(self, arr):
        N = len(arr)
        self.N = N
        self.size = 1
        self.arr = arr
        while self.size < N:
            self.size *= 2
        
        self.tree = [0] * (2*self.size)

        self._build(1, 0, self.N-1)

    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.tree[node]
        mid = (left+right)//2

        self.tree[node] = self._build(node*2,left,mid) + self._build(node*2+1, mid+1, right)
        return self.tree[node]

    def update(self, index, value):
        self._update(1, 0, self.N - 1, index, value)

    def _update(self, node, left, right, index, value):
        if left == right:
            self.arr[index] = value
            self.tree[node] = value
            return

        mid = (left + right)//2

        if index <= mid:
            self._update(node * 2, left, mid, index, value)
        else:
            self._update(node * 2 + 1, mid+1, right, index, value)

        self.tree[node] = self.tree[node*2]+self.tree[node*2+1]

    def query(self, left, right):
        return self._query(1, 0, self.N-1,left, right)


    def _query(self, node, l, r, left, right):
        if right < l or left > r:
            return 0

        if left <= l and r <= right:
            return self.tree[node]

        mid = (l+r)//2

        return self._query(node*2,l,mid,left, right) + self._query(node*2+1, mid+1,r, left, right)


# 2. 비재귀 새그먼트 트리
class IterativeSegmentTree:
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr
        self.size = 1

        # size는 n이상인 가장 작은 2의 거듭제곱임
        while self.size < self.N:
            self.size *= 2

        self.tree = [0] * (2 * self.size)
        
        # Leaf에 원본 배열 저장
        for i in range(self.N):
            self.tree[self.size+i] = arr[i]

        # 내부 노드 구성
        for i in range(self.size -1, 0, -1):
            self.tree[i] = self.tree[i * 2] + self.tree[i * 2 + 1]


    def update(self,index, value):
        pos = self.size + index
        self.tree[pos] = value

        pos //= 2
        while pos >= 1:
            self.tree[pos] = self.tree[pos * 2] + self.tree[pos * 2 + 1]
            pos //= 2


    def query(self, left, right):
        left += self.size
        right += self.size

        result = 0

        while left <= right:
            if left % 2 == 1:
                result += self.tree[left]
                left += 1

            if right % 2 == 0:
                result += self.tree[right]
                right -= 1

            left //= 2
            right //= 2

        return result


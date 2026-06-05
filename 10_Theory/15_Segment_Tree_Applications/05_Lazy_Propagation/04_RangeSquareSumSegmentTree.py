
class RangeSquareSumSegmentTree:
    '''
    다음 2개의 연산을 하는 세그먼트 트리 구현하기
    Update : [l, r]에 대해서 A를 더하기
    Query : [l, r]의 구간 제곱 합을 구하기

    [접근법] : [i,j]에 A를 더한 후 제곱합 - [i,j]의 제곱합 = 2Ax_i + A^2
    => 그럼 구간 업데이트(X+A)는 기존 X 제곱 합 + 2 * 구간 합 * A + A^2 * length를 해주면 된다.
    '''
    def __init__(self, arr):
        self.arr = arr
        self.N = len(arr)
        self.size = 1

        while self.size < self.N:
            self.size *= 2
        
        self.square_sum = [0] * (2 * self.size)
        self.normal_sum = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)

        self._build(1, 0, self.N-1)
    
    def _build(self, node, left, right):
        if left == right:
            self.square_sum[node] = self.arr[left] ** 2
            self.normal_sum[node] = self.arr[left]
            return
        
        mid = (left + right) // 2
        self._build(node*2, left, mid)
        self._build(node*2+1,mid+1,right)

        self.normal_sum[node] = self.normal_sum[node*2] + self.normal_sum[node*2+1]
        self.square_sum[node] = self.square_sum[node*2] + self.square_sum[node*2+1]


    def _apply(self, node, left, right, value):
        length = right - left + 1
        self.lazy[node] += value
        self.square_sum[node] += self.normal_sum[node] * 2 * value + (value ** 2) * length
        self.normal_sum[node] += value * length
    
    def _push(self, node, left ,right):
        if self.lazy[node] == 0:
            return
        
        if left == right:
            return

        mid = (left + right) // 2
        value = self.lazy[node]
        self._apply(node*2, left,mid, value)
        self._apply(node*2+1,mid+1, right,value)
        self.lazy[node] = 0


    def _update(self, node, left, right, l, r, v):
        if right < l or r < left:
            return

        if l <= left and right <= r:
            self._apply(node, left, right, v)
            return 
        
        self._push(node, left, right)
        
        mid = (left + right) // 2
        self._update(node * 2, left, mid, l, r, v)
        self._update(node * 2+1, mid+1, right, l, r, v)

        self.normal_sum[node] = self.normal_sum[node * 2] + self.normal_sum[node * 2 + 1]
        self.square_sum[node] = self.square_sum[node * 2] + self.square_sum[node * 2 + 1]

    def _query(self, node, left, right, l, r):
        if right < l or r < left:
            return 0 

        if l <= left and right <= r:
            return self.square_sum[node]
        
        self._push(node, left, right)
        mid = (left + right) // 2
        return self._query(node * 2, left, mid, l, r) + self._query(node * 2 + 1, mid + 1, right, l, r)

    def update(self, l, r, v):
        self._update(1, 0, self.N-1 , l, r, v)

    def query(self, l, r):
        return self._query(1, 0, self.N-1, l, r)
    
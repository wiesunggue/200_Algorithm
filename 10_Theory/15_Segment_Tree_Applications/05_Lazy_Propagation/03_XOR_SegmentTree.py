import sys
sys.setrecursionlimit(10**5)


class XORSegmentTree:
    ''' 
        구간 XOR 연산 쿼리 + 구간 합에 대한 세그먼트 트리
        값의 범위는 21억 이하로 제한한다.(2^32 미만)
    '''
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr
        self.size = 1

        while self.size < self.N:
            self.size *= 2

        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self.bit_count = [[0] * 32 for i in range(2 * self.size)]

        self._build(1,0,self.N-1)

    def _build(self,node, left, right):
        if left == right:
            self.tree[node] = self.arr[left]
            self.bit_count[node] = self._bitCount(self.arr[left])
            return 
        
        mid = (left + right) // 2
        self._build(node * 2, left, mid)
        self._build(node * 2 + 1, mid + 1, right)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]
        self.bit_count[node] = self._bit_count_Add(node*2, node*2+1)
        
    def _push(self,node, left, right):
        if self.lazy[node] == 0:
            return
        if left == right:
            return
        
        value = self.lazy[node]
        mid = (left + right)//2
        self._apply(node*2, left, mid, value)
        self._apply(node*2+1, mid+1, right, value)
        self.lazy[node] = 0

    def _apply(self, node, left, right, value):
        length = right - left + 1
        self.lazy[node] ^= value
        for i in range(32):
            if value & (1 << i):
                self.bit_count[node][i] = length - self.bit_count[node][i]

        self.tree[node] = sum(
        self.bit_count[node][i] * (1 << i)
        for i in range(32))

    def _update(self, node, left, right, l, r, v):
        if right < l or r < left:
            return
        if l <= left and right<=r:
            self._apply(node,left,right,v)
            return
        
        self._push(node,left,right)
        mid = (left + right) // 2
        self._update(node*2,left,mid,l,r,v)
        self._update(node*2+1,mid+1,right,l,r,v)

        self.tree[node] = self.tree[node*2] + self.tree[node*2+1]
        self.bit_count[node] = self._bit_count_Add(node*2,node*2+1)
        
    def _query(self, node, left, right, l, r):
        if right < l or r < left:
            return 0
        if l <= left and right<=r:
            return self.tree[node]
        
        self._push(node,left,right)
        mid = (left + right) // 2

        return self._query(node*2,left,mid,l,r) + self._query(node*2+1,mid+1,right,l,r)
    
    def _bit_count_Add(self, node1, node2):
        bit_count = [0] * 32
        for i in range(32):
            bit_count[i] = self.bit_count[node1][i] + self.bit_count[node2][i]
        
        return bit_count
    
    def _bitCount(self, value):
        '''값을 넣으면 2진수로 bit count 배열에 넣는 함수'''
        bit = [0] * 32
        for i in range(32):
            bit[i] =1 if value & (1<<i) != 0 else 0
        return bit
    

    def update(self, l, r, v):
        self._update(1, 0 ,self.N-1, l, r, v)
    def query(self, l, r):
        return self._query(1, 0, self.N-1, l, r)
    

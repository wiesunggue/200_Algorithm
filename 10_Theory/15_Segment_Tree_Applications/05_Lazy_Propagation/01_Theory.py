'''Range Query의 경우 다음과 같은 연산이 가능하다
1. Max Query + Range Add
2. Max Query + Range Assign
3. Range Sum + Range Assign
4. Range Sum + Range Assign + Range Add
5. Range Sum + Range Multiply
6. Range Sum + Range Affine
7. Range XOR + Range XOR
8. Range Sum + Range XOR
9. First Position Query(k이상인 수 중 가장 왼쪽) + Range Add
10. Range Sum of Square + Range Add
11. Range GCD + Range Add
'''

import sys
sys.setrecursionlimit(10**5)

class RecursivLazySegmentTree:
    '''1. Max Query와 Range Add Update Query 를 가진 세그먼트 트리'''
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr
        self.size = 1

        while self.size < self.N:
            self.size *= 2
        
        self.tree = [-10**10] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        self.haslazy = [False] * (2 * self.size)

        self._build(1,0,self.N-1)
    def _build(self, node, left, right):
        if left == right:
            self.tree[node] = self.arr[left]
            return self.tree[node]
        
        mid = (left + right) // 2
        self.tree[node] = max(self._build(node*2,left,mid),self._build(node*2+1,mid+1,right))
        return self.tree[node]

    def _query(self, node, left, right, l, r):
        if right<l or r < left:
            return -10**10
        
        if l<=left and right<=r:
            return self.tree[node]
        
        self._push(node, left, right)
        mid = (left + right) // 2
        return max(self._query(node*2, left, mid,l,r), self._query(node*2+1, mid+1, right,l,r))
    
    def _update(self, node, left, right, l, r, value):
        if right<l or r < left:
            return 
        
        if l<=left and right<=r:
            self._apply(node, left, right, value)
            return 

        self._push(node, left, right)
        mid = (left + right) // 2
        self._update(node*2,left,mid,l,r,value)
        self._update(node*2+1,mid+1,right,l,r,value)

        self.tree[node] = max(self.tree[node * 2],self.tree[node * 2 + 1])

    def _apply(self, node, left, right, value):
        '''Lazy하도록 적용하는 함수'''
        self.haslazy[node] = True
        self.lazy[node] += value
        self.tree[node] += value


    def _push(self, node, left, right):
        '''하위 노드에 Lazy를 전달하는 함수'''
        if not self.haslazy[node]:
            return
        if left == right:
            return
        value = self.lazy[node]
        mid = (left + right) // 2
        self._apply(node * 2, left, mid, value)
        self._apply(node * 2 + 1, mid+1, right, value)
        self.lazy[node] = 0
        self.haslazy[node] = False

    def update(self, l, r, value):
        '''[l,r]구간에 모두 value를 더하는 함수'''
        self._update(1,0,self.N-1,l,r,value)

    def query(self, l, r):
        '''주어진 구간 중 가장 큰 수를 찾는 함수'''
        return self._query(1,0,self.N-1,l,r)


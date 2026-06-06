import os
import sys
sys.setrecursionlimit(10**6)

input = sys.stdin.readline

class segmentTree:
    def __init__(self,N,arr):
        self.N = N
        self.tree = [0] * (4*N)
        self.initial_arr = arr
        self.initialize(0,N-1,1)
    def initialize(self, left,right,node):
        if left == right:
            self.tree[node] = self.initial_arr[left]
            return self.tree[node]
        mid = (left + right)//2
        left_data = self.initialize(left,mid,node*2)
        right_data = self.initialize(mid+1,right, node*2+1)

        self.tree[node] = max(left_data,right_data)
        return self.tree[node]

    def inner_query(self,left,right,node,nodeleft,noderight):
        if right<nodeleft or noderight < left:
            return -10**10
        if left <= nodeleft  and noderight <= right:
            return self.tree[node]
        mid = (nodeleft+noderight)//2

        return max(self.inner_query(left,right,node*2,nodeleft,mid),self.inner_query(left,right,node*2+1,mid+1,noderight))

    def inner_update(self,index,value, node, nodeleft,noderight):
        if index < nodeleft or noderight <index:
            return self.tree[node]
        if nodeleft == noderight:
            self.tree[node] = value
            return self.tree[node]
        mid = (nodeleft+noderight)//2
        self.tree[node] = max(self.inner_update(index,value,node*2,nodeleft,mid), self.inner_update(index,value,node*2+1, mid+1,noderight))
        return self.tree[node]

    def update(self, index, value):
        return self.inner_update(index, value, 1, 0, self.N - 1)

    def query(self, left, right):
        return self.inner_query(left, right, 1, 0, self.N - 1)

N = int(input())
arr = list(map(int,input().split()))

seg = segmentTree(N,arr)

start, end = 0,1
ans = 0
psum = [0] * (N+1)
for i in range(N):
    psum[i] = arr[i] + psum[i-1]

print(psum)
cut_off = -1
max_value = 0
max_pos = 0
for i in range(N):
    if psum[i] < 0:
        cut_off = i
        max_value = 0
    if max_value <= psum[i]:
        max_pos = i
        max_value = psum[i]
        print(ans, max_value, psum[cut_off],seg.query(cut_off,i))
        ans = max(ans, max_value - psum[cut_off] - seg.query(cut_off,i))

print(ans)
# https://www.acmicpc.net/problem/14428
# 수열과 쿼리 16

class segmentTree:
    def __init__(self,N,arr):
        self.N = N
        self.tree = [0] * (4*N)
        self.initial_arr = arr
        self.initialize(0,N-1,1)
    def initialize(self, left,right,node):
        if left == right:
            self.tree[node] = self.initial_arr[left],left
            return self.tree[node]
        mid = (left + right)//2
        left_data = self.initialize(left,mid,node*2)
        right_data = self.initialize(mid+1,right, node*2+1)

        self.tree[node] = min(left_data,right_data)
        return self.tree[node]

    def inner_query(self,left,right,node,nodeleft,noderight):
        if right<nodeleft or noderight < left:
            return 10**10,-1
        if left <= nodeleft  and noderight <= right:
            return self.tree[node]
        mid = (nodeleft+noderight)//2

        return min(self.inner_query(left,right,node*2,nodeleft,mid),self.inner_query(left,right,node*2+1,mid+1,noderight))

    def inner_update(self,index,value, node, nodeleft,noderight):
        if index < nodeleft or noderight <index:
            return self.tree[node]
        if nodeleft == noderight:
            self.tree[node] = value,nodeleft
            return self.tree[node]
        mid = (nodeleft+noderight)//2
        self.tree[node] = min(self.inner_update(index,value,node*2,nodeleft,mid), self.inner_update(index,value,node*2+1, mid+1,noderight))
        return self.tree[node]

    def update(self, index, value):
        return self.inner_update(index, value, 1, 0, self.N - 1)

    def query(self, left, right):
        return self.inner_query(left, right, 1, 0, self.N - 1)

N = int(input())
arr = list(map(int,input().split()))
tree = segmentTree(N,arr)
M = int(input())
for i in range(M):
    query = list(map(int,input().split()))
    if query[0] == 1:
        tree.update(query[1]-1,query[2])
    else:
        print(tree.query(query[1]-1,query[2]-1)[1]+1)


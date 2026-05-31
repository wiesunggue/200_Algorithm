import random
import sys
import heapq
sys.setrecursionlimit(10**5)
input = sys.stdin.readline
test_mode = False

N,K = map(int,input().split())
if test_mode:
    arr = [random.randint(1,10**9) for i in range(N)]
else:
    arr = list(map(int, input().split()))
pq = []
# Union Find
class OptimizedDisjointSet():
    def __init__(self,size):
        self.parent = [i for i in range(size)]
        self.rank = [1 for i in range(size)]
        self.N = size

    def find(self,u):
        if u==self.parent[u]:
            return u
        return self.find(self.parent[u])

    def merge(self,u,v):
        u,v = self.find(u),self.find(v)
        if u==v:
            return
        if self.rank[u]>self.rank[v]:
            u,v = v,u

        self.parent[u]=v
        if self.rank[u]==self.rank[v]:
            self.rank[v]+=1

# Sag Tree
tree = [0]*2*N

def update(index, value):
    index += N
    tree[index] = value

    while index > 1:
        index //= 2
        tree[index] = max(tree[index * 2] , tree[index * 2 + 1])


def query(left, right):
    result = -10**10
    left += N
    right += N

    while left < right:
        if left % 2 == 1:
            result = max(result, tree[left])
            left += 1
        left //= 2

        if right % 2 == 1:
            right -= 1
            result = max(result, tree[right])
        right //= 2
    return result

# 구간 쿼리
for i in range(N):
    update(i,arr[i])

#
for i in range(N):
    if i+K==N:
        break
    heapq.heappush(pq,(query(i,i+K+1),i,i+K))
union = OptimizedDisjointSet(N)

cost = 0
count = 1
iteration = 0
while pq:
    iteration += 1
    if count == N:
        break
    value, left, right = heapq.heappop(pq)
    if union.find(left) != union.find(right):
        cost += value
        union.merge(left,right)
        count += 1
        print(f"append : {value} {left} {right}")

    if right+1<N and union.find(left) != union.find(right+1):
        heapq.heappush(pq, (max(value,arr[right+1]),left, right+1))


print(cost if count == N else -1)
if test_mode:
    print("iteration : ",iteration)

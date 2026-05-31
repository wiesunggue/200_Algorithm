# 간단한 알고리즘 요약 정리

#   다이나믹 프로그래밍(DP)
#   그래프 최단 경로: 다익스트라 알고리즘(Dijkstra’s Algorithm)
#   위상 정렬(Topological Sort)
#   세그먼트 트리(Segment Tree)
#   그래프 최단 경로: 벨만 포드, 플로이드 와샬 알고리즘
#   이분 매칭(Bipartite Matching)
#   펜윅 트리(Fenwick Tree)
#   유니온 파인드(Union-Find)

# 유니온 파인드
class disjointSet:
    def __init__(self,N):
        self.N = N
        self.rank = [1]*N
        self.parent = [i for i in range(N)]

    def find(self,u):
        if self.parent[u] == u:
            return u
        return self.find(self.parent[u])
    def merge(self,u,v):
        u,v = self.find(u),self.find(v)
        if u==v:
            return
        if self.rank[u]<self.rank[v]: # 항상 u가 더 큼
            u,v = v,u

        self.parent[v] = u
        if self.rank[u] == self.rank[v]:
            self.rank[u] += 1

# 펜윅 트리
class FenwickTree:
    def __init__(self,N):
        self.N = N
        self.tree = [0] * N

    def segAdd(self,pos,v):
        pos +=1
        while pos<self.N:
            self.tree[pos] += v
            pos += pos & -pos

    def segSum(self,pos):
        # 처음부터 pos까지 합하는 함수
        pos += 1
        ret = 0
        while pos:
            ret += self.tree[pos]
            pos &= pos-1

# 플로이드 워셜
N = 10
arr = [[10**10]*N for i in range(N)]
for k in range(N):
    for i in range(N):
        if arr[i][k] == 10**10:
            continue
        for k in range(N):
            arr[i][j] = min(arr[i][j],arr[i][k]+arr[k][j])

# 위상 정렬
# 위상 정렬 구현 방식 - 저장공간 할당과 dfs 뒤집기

# 저장공간 할당은 큐, 스택, 우선순위 큐를 활용하여 구현한다
# dfs뒤집기는 dfs 탐색 종료 순서를 기준으로 값을 저장하고 이를 뒤집어서 위상정렬을 진행한다.

# 저장공간 할당 방식
# table을 이용해서 진입차수가 0일 때만 탐색 허용
# 이외에는 bfs 랑 똑같음

from collections import deque
#N, M = map(int,input().split())
graph = [[] for i in range(N+1)] # 연결을 저장하는 그래프
table = [0] * (N+1)  # 차수를 저장하는 테이블
for i in range(M):
    #a,b = map(int,input().split())
    graph[a].append(b)
    table[b] += 1
print(table)
def topological_sort():
    global table
    dq = deque()
    result = [0] * (N+1)
    for i in range(1,N+1):
        if table[i] == 0:
            dq.append((i,1))
            result[i] = 1
    while dq:
        node,r = dq.popleft()
        for i in graph[node]:
            table[i] -= 1
            if table[i] == 0:
                result[i] = r+1
                dq.append((i,r+1))
    print(*result[1:],sep=' ')

topological_sort()

# dfs 구현 방식은 탐색 순서의 역순

visit = [0] * N
order = []
def dfs(n): # 모든 출발점에 대해서 탐색해주어야 함
    for i in graph[n]:
        if visit[i] == 0:
            visit[i] = 1
            dfs(i)

    order.append(n)

for i in range(N):
    if visit[i] == 0:
        dfs(i)

order = reversed(order) # dfs 탐색 순서의 역순

# 세그먼트 트리
class SegmentTree:
    def __init__(self, N):
        self.N = N
        self.arr = [0] * (4 * N)
        self.initialarr = [0] * N

    def initialize(self, left, right, node):
        if left == right:
            self.arr[node] = self.initialarr[left]
            return self.arr[node]
        mid = (left + right) // 2
        leftdata = self.initialize(left, mid, node * 2)
        rightdata = self.initialize(mid + 1, right, node * 2 + 1)

        self.arr[node] = leftdata + rightdata
        return self.arr[node]

    def innerquery(self, left, right, node, nodeleft, noderight):
        # 범위 넘어가는 경우 탐색 중지
        if right < nodeleft or noderight < left:
            return 0
        if left <= nodeleft and noderight <= right:
            return self.arr[node]
        mid = (nodeleft + noderight) // 2

        return self.innerquery(left, right, node * 2, nodeleft, mid) + self.innerquery(left, right,node * 2 + 1, mid + 1,noderight)

    def innerupdate(self, index, value, node, nodeleft, noderight):
        if index < nodeleft or noderight < index:
            return 0

        if nodeleft == noderight:
            self.arr[node] = value
            return self.arr[node]

        mid = (nodeleft + noderight) // 2
        self.arr[node] = self.innerupdate(index, value, node*2, nodeleft, mid) + self.innerupdate(index, value,node*2+1,mid+1, noderight)
        return self.arr[node]

    def update(self, index, value):
        return self.innerupdate(index, value, 1, 0, self.N - 1)

    def query(self, left, right):
        return self.innerquery(left, right, 1, 0, self.N - 1)


# 이분 매칭

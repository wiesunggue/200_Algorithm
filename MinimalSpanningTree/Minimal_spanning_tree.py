# https://www.acmicpc.net/problem/1197
# 최소 스패닝 트리

# 크루스칼 방식
class UnionFind:
    def __init__(self,N):
        self.N = N
        self.Parent = [i for i in range(N)]
        self.Rank = [1 for i in range(N)]

    def Find(self,u):
        if self.Parent[u] == u:
            return u
        return self.Find(self.Parent[u])

    def merge(self,u,v):
        u,v = self.Find(u), self.Find(v)

        if u == v:
            return False

        if self.Rank[u] < self.Rank[v]:
            u, v = v, u
        self.Parent[v] = u
        if self.Rank[u] == self.Rank[v]:
            self.Rank[u] += 1

        return True

V, E = map(int,input().split())

edges = [list(map(int,input().split())) for i in range(E)]

edges.sort(key = lambda x: x[2])
ans = 0
union = UnionFind(V)
for i in range(E):
    if union.merge(edges[i][0],edges[i][1]):
        ans += edges[i][2]

print(ans)
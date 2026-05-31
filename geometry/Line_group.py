# https://www.acmicpc.net/problem/2162
# 선분 그룹
from collections import defaultdict


# 선분 구분 절차
# 1. 방향 함수 정의(orient)
# 2. 교차 판정 알고리즘(pseudocode)
# orient(A,B,C) != orient(A,B,D) 이고
# orient(C,D,A) != orient(C,D,B) 이면 교차 선분
# 3. 특수 케이스(점이 만나는 경우) 조사
class Position:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def sign(x):
    return 0 if x==0 else (1 if x>0 else -1)

def orient(P, Q, R):
    # sign((Q−P)×(R−P)) 으로 판정
    val = (Q.x-P.x)*(R.y-P.y) - (Q.y-P.y)*(R.x-P.x) # 외적 연산
    return sign(val)

def included(P,Q,R):
    # PQ위에 한 점이 포함되는 경우
    return min(P.x,Q.x) <= R.x <= max(P.x,Q.x) and \
           min(P.y,Q.y) <= R.y <= max(P.y,Q.y)

def pseudocode(A,B,C,D):
    # 선분 AB와 CD가 교차하는지 판정하기
    o1, o2 = orient(A,B,C), orient(A,B,D)
    o3, o4 = orient(C,D,A), orient(C,D,B)
    if o1 != o2 and o3 != o4:
        return True # 교차하는 경우

    # 특수 케이스: 공평 + 사각형 포함 여부
    if o1==0 and included(A,B,C): return True
    if o2==0 and included(A,B,D): return True
    if o3==0 and included(C,D,A): return True
    if o4==0 and included(C,D,B): return True
    return False

class DisJointSet:
    def __init__(self,size):
        self.size = size
        self.parent = [i for i in range(size)]
        self.rank = [1 for i in range(size)]
        self.capacity = [1 for i in range(size)]
    def find(self,u):
        if u == self.parent[u]:
            return u
        return self.find(self.parent[u])

    def merge(self,u,v):
        u,v = self.find(u), self.find(v)
        if u==v:
            return
        # rank는 항상 u가 더 크다
        if self.rank[u] < self.rank[v]:
            u,v = v,u

        self.parent[v] = u
        self.capacity[u] += self.capacity[v]

        if self.rank[u] == self.rank[v]:
            self.rank[u] += 1

    def DisJoint(self):
        d = defaultdict(int)
        for i in range(self.size):
            d[self.find(i)] += 1

        return d
N = int(input())
dis = DisJointSet(N)
arr = [list(map(int,input().split())) for i in range(N)]

for i in range(N):
    for j in range(N):
        if i == j:
            continue
        A, B = Position(arr[i][0],arr[i][1]), Position(arr[i][2],arr[i][3])
        C, D = Position(arr[j][0],arr[j][1]), Position(arr[j][2],arr[j][3])
        if pseudocode(A,B,C,D):
            dis.merge(i,j)

print(len(dis.DisJoint()))
print(max(dis.capacity))
# https://www.acmicpc.net/problem/1167
# 트리의 지름 1167
import sys
sys.setrecursionlimit(10**5+100)
input = sys.stdin.readline

N = int(input())
graph = [[] for i in range(N+1)]
for i in range(N):
    data = list(map(int,input().split()))
    idx = 1
    while data[idx] != -1:
        graph[data[0]].append((data[idx],data[idx+1]))
        idx += 2

print(*graph,sep='\n')
visit = [0] * (N + 1)
maxDist,maxNode = 0,0
def dfs(node,dist):
    global maxDist,maxNode,visit
    if maxDist < dist:
        maxDist = dist
        maxNode = node
    for i in range(len(graph[node])):
        n,w = graph[node][i]
        if visit[n] == 1:
            continue
        visit[n] = 1
        dfs(n,dist+w)

def findMaxDist():
    global maxDist,maxNode,visit
    maxDist, maxNode = 0, 0
    startNode = 1
    visit[startNode] = 1
    dfs(startNode,0)

    startNode = maxNode
    visit = [0] * (N + 1)
    visit[startNode] = 1
    maxDist, maxNode = 0, 0
    dfs(startNode,0)
    return maxDist

print(findMaxDist())
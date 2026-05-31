# https://www.acmicpc.net/problem/28707
# 배열 정렬 문제
import heapq
from itertools import permutations
from collections import Counter

N = int(input())
arr = list(map(int,input().split()))
M = int(input())
change = [list(map(int,input().split())) for i in range(M)]

IndexToValue = []
ValueToIndex = {}
for idx,value in enumerate(sorted(set(list(permutations(arr,N))))):
    IndexToValue.append(value)
    ValueToIndex[value] = idx

def dijkstra():
    pq = []
    startIndex = ValueToIndex[tuple(arr)]
    heapq.heappush(pq,(0,startIndex))
    MAX_VAL = 10**10
    table = [MAX_VAL] * len(IndexToValue)
    table[startIndex] = 0
    while pq:
        cost, index = heapq.heappop(pq)
        value = IndexToValue[index]
        if table[index] < cost:
            continue

        for i in range(M):
            x,y,c = change[i]
            data = list(value)
            data[x-1],data[y-1] = data[y-1],data[x-1]
            newIndex = ValueToIndex[tuple(data)]
            if table[newIndex] <= cost + c:
                continue
            table[newIndex] = cost + c
            heapq.heappush(pq,(table[newIndex],newIndex))
    if(table[0] == MAX_VAL):
        return -1
    else:
        return table[0]
def isDecreasing(arr):
    for i in range(1, len(arr)):
        if arr[i]>arr[i-1]:
            return False
    return True

print(dijkstra())
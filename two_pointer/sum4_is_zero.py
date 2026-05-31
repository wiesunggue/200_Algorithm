# https://www.acmicpc.net/problem/7453
# 백준 합이 0인 네 정수
from collections import defaultdict
N = int(input())
A,B,C,D = [],[],[],[]
for i in range(N):
    arr = list(map(int,input().split()))
    A.append(arr[0])
    B.append(arr[1])
    C.append(arr[2])
    D.append(arr[3])

AplusB = defaultdict(int)

for i in range(N):
    for j in range(N):
        AplusB[A[i]+B[j]] += 1

ans = 0
for i in range(N):
    for j in range(N):
        if AplusB.get(-C[i]-D[j]) != None:
            ans += AplusB[-C[i]-D[j]]

print(ans)
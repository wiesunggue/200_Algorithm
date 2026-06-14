import sys
input = sys.stdin.readline

N = int(input())
arr = [list(map(int,input().split())) for i in range(N)]

arr.sort()
lower = 10**10
ans = 0
for i in range(N):
    if arr[i][1] < lower:
        ans += 1
        lower = arr[i][1]

print(ans)
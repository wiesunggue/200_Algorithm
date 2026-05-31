# https://www.acmicpc.net/problem/2342
# 백준 2342번 Dance Dance Revolution
inf = 10**10
arr = list(map(int,input().split()))
N = len(arr)

dp =[[[inf for k in range(5)] for j in range(5)] for i in range(N)]
dp[0][0][0] = 0
cost = [[1,2,2,2,2],
        [2,1,3,4,3],
        [2,3,1,3,4],
        [2,4,3,1,3],
        [2,3,4,3,1]]

for i in range(1,N):
    for j in range(5):
        for k in range(5):
            if i==j:
                continue
            move_to = arr[i-1]
            # j를 움직이는 경우
            if k != move_to:
                dp[i][move_to][k] = min(dp[i][move_to][k],dp[i-1][j][k]+cost[j][move_to])
            # k를 움직이는 경우
            if j != move_to:
                dp[i][j][move_to] = min(dp[i][j][move_to],dp[i-1][j][k]+cost[k][move_to])

print(min(map(min,dp[N-1])))
print(dp[N-1])
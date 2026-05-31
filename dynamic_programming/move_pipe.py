# https://www.acmicpc.net/problem/17070
# 파이프 옮기기

N = int(input())
arr = [list(map(int,input().split())) for i in range(N)]
dp = [[[0]*3 for i in range(N)] for j in range(N)]
dp[0][1][0] = 1 # 초기 방향

direction = [0,1,2] # 0은 왼쪽 위 1는 대각선 2은 아래방향

for i in range(N):
    for j in range(1,N):
        for k in range(3):
            if arr[i][j] == 1:
                continue

            if k == 0:
                dp[i][j][k] += dp[i][j-1][0] + dp[i][j-1][1]
            elif k == 1 and arr[i][j-1] == 0 and arr[i-1][j] == 0:
                dp[i][j][k] += dp[i-1][j-1][0] + dp[i-1][j-1][1] + dp[i-1][j-1][2]
            elif k == 2:
                dp[i][j][k] += dp[i-1][j][1] + dp[i-1][j][2]

print(*dp,sep='\n')
print(sum(dp[-1][-1]))
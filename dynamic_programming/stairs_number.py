# https://www.acmicpc.net/problem/1562
# 백준 게단 수 문제
N = int(input())

dp = [[[0]*10 for j in range(1<<10)] for i in range(N)]
MOD = 1000000000
for j in range(1,10):
    dp[0][1<<j][j] = 1

# dp [길이, 0~10 포함여부, 끝자리] = 개수
for t in range(1,N): # 자리수 배열
    for i in range(1<<10): # 0~10 포함여부 집합 S
        for j in range(10): # 끝나는 숫자
            nxt = i | (1<<j)
            if j != 0:
                dp[t][nxt][j] += dp[t-1][i][j-1]
            if j != 9:
                dp[t][nxt][j] += dp[t-1][i][j+1]
            dp[t][nxt][j] %= MOD

print(dp[N-1][(1<<10)-1])
print(sum(dp[N-1][(1<<10)-1])%MOD)
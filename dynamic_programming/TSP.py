# https://www.acmicpc.net/problem/2098
# 백준 외판원 순회 문제

# N개의 도시르 모두 거쳐서 원래 도시로 최소비용으로 돌아오는 방법(중복 방문 금지)
# A->B의 비용과 B->A의 비용이 다름
# 1. 조기 종료
# 2. 탐색 순서 변화(그리디한 탐색)
# 3. 간단한 휴리스틱(낙관적인 탐색- 가장 먼곳까지 더했을 때 최적해보다 크다면 조기종료)
# 4. 지나온 경로에 대한 가지치기(인접한 두 경로를 바꾸기)
# 5. 마지막 단계 메모이제이션 하기(일부 결과 저장)

N = int(input())
CostMatrix = [list(map(int,input().split())) for i in range(N)]
Dp = []
Visit = 0
INF = 10**9

def HeldKarp():
    """Held Karp 이론에 의한 풀이 O(N^2 * 2^N)"""

    dp = [[INF for j in range(N)] for i in range(1<<N)]

    for i in range(1,N):
        if CostMatrix[0][i] != 0:
            dp[1<<i][i] = CostMatrix[0][i]

    for m in range(1,1<<N):
        for j in range(N):
            if not (m & (1<<j)):
                continue
            for i in range(N):
                if not (m & (1<<i)) and CostMatrix[j][i]:
                    nxt = m | (1<<i)
                    dp[nxt][i] = min(dp[nxt][i],dp[m][j]+CostMatrix[j][i])

    ans = INF
    for i in range(1,N):
        if CostMatrix[i][0] != 0:
            ans = min(ans,dp[(1<<N)-2][i]+CostMatrix[i][0])

    return ans

print(HeldKarp())
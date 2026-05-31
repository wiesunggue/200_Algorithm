# https://www.acmicpc.net/problem/1202
# 백준 보석 도둑

import heapq

N,K = map(int,input().split())

jewel = [list(map(int,input().split())) for i in range(N)]
bag = [int(input()) for i in range(K)]

# 보석을 무게 기준으로 정렬
jewel.sort()

# 가방을 무게 기준으로 정렬
bag.sort()

# 가방 무게보다 무게가 적은 보석 중 최대 가치의 보석 훔치기
pq = []
idx = 0
ans = 0
for i in range(K):
    while idx<N and jewel[idx][0] <= bag[i]:
        heapq.heappush(pq, -jewel[idx][1])
        idx += 1
    if len(pq)!= 0:
        ans -= heapq.heappop(pq)

print(ans)
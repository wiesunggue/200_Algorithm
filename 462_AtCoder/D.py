import heapq

N, D = map(int, input().split())

time = [list(map(int,input().split())) for i in range(N)]

# y에 대해 정렬
time.sort(key=lambda x: x[1])

pq = []
for i in range(N):
    heapq.heappush(time[i][0])
    if len(pq) >= 2:
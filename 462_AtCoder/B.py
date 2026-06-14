N = int(input())
arr = []
ans = [[] for i in range(N+1)]
for i in range(N):
    t = list(map(int, input().split()))[1:]
    for j in range(len(t)):
        ans[t[j]].append(str(i+1))

for i in range(1,N+1):
    print(len(ans[i]), ' '.join(ans[i]))


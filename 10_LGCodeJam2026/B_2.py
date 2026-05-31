import sys
sys.setrecursionlimit(10**5)
input = sys.stdin.readline
test_mode = False

N = int(input())
arr = list(map(int,input().split()))

# Sag Tree
tree = [-10**10]*2*N

def update(index, value):
    index += N
    tree[index] = value

    while index > 1:
        index //= 2
        tree[index] = max(tree[index * 2] , tree[index * 2 + 1])


def query(left, right):
    if(left==right):
        return 0
    result = -10**10
    left += N
    right += N

    while left < right:
        if left % 2 == 1:
            result = max(result, tree[left])
            left += 1
        left //= 2

        if right % 2 == 1:
            right -= 1
            result = max(result, tree[right])
        right //= 2
    return result

for i in range(N):
    update(i, arr[i])

start, end = 0, 0
cost = 0
ans = 0

dp1 = [[0,0,0] for i in range(N)]
dp2 = [[0,0,0] for i in range(N)]
dp1[0] = [arr[0],0,0]
dp2[0] = [arr[0],0,0]
for i in range(1,N):
    if dp1[i-1][0] > 0:
        dp1[i] =  [dp1[i-1][0] + arr[i],dp1[i-1][1],i]
    else:
        dp1[i] = [arr[i],i,i]

for i in range(1,N):
    after = query(dp1[i-1][1],i+1)

    # 최대값을 만나는 경우
    if arr[i] == after:
        dp2[i] = [dp1[i-1][0]+arr[i],dp1[i-1][1],i]
    else:
        # dp2가 음수가 되는 경우
        if dp2[i-1][0]-query(dp2[i-1][1],dp2[i-1][2]) < 0:
            dp2[i] = [arr[i],i,i]
        else:
            dp2[i] = [dp2[i-1][0]+arr[i],dp2[i-1][1],i]

ans = 0
for i in range(N):
    print(dp2[i][0],dp2[i][1],dp2[i][2],query(dp2[i][1],dp2[i][2]+1))
    ans = max(ans,dp2[i][0]-query(dp2[i][1],dp2[i][2]+1))

print(ans)
print(dp1)
print(dp2)
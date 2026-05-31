import sys
sys.setrecursionlimit(10**5)
input = sys.stdin.readline
test_mode = False

N = int(input())
arr = list(map(int,input().split()))

# Sag Tree
tree = [-10**10]*2*(N)

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

def devide_conquer(left, right):
    print(left, right)
    if left == right:
        return 0, left, right, arr[left]
    mid = (left+right)//2
    mid_max = 0
    # Left
    left_node = devide_conquer(left, mid)

    # Right
    right_node = devide_conquer(mid+1, right)
    print(left_node, right_node)
    # Mid
    # Left Contain Mid
    lv = left_node[0]
    ll = left_node[1]
    lr = left_node[2]+1
    lm = left_node[3]
    ls = [lv,ll,lr,lm]
    while lr <= right:
        if lm < arr[lr]:
            lv = lv + lm
            ls[0] = lv
            ls[3] = arr[lr]
            lm = arr[lr]
        else:
            if ls[0] < lv + arr[lr]:
                ls[0] = lv+arr[lr]
                ls[2] = lr
            lv += arr[lr]
        lr += 1

    rv = right_node[0]
    rl = right_node[1]-1
    rr = right_node[2]
    rm = right_node[3]
    rs = [rv,rl, rr, rm]
    while rl >= left:
        if rm < arr[rl]:
            rv = rv + rm
            rs[0] = rv
            rs[3] = arr[rl]
        else:
            if rs[0] < rv + arr[rl]:
                rs[0] = rv + arr[rl]
                rs[2] = rl
            rv += arr[rl]
        rl -= 1
    print(ls, rs)
    if ls[0] > rs[0]:
        return ls
    else:
        return rs

print(devide_conquer(0,N-1))
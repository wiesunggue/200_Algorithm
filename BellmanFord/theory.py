N = int(input())
arr = list(map(int,input().split()))
countFruits = [0] * 10

def remains():
    cnt = 0
    for i in range(len(countFruits)):
        if countFruits[i] != 0:
            cnt += 1
    return cnt

start,end = 0,0
ans = 0
while start<=end and end<N:
    rem = remains()
    if rem <= 2:
        countFruits[arr[end]] += 1
        end += 1
    else:
        countFruits[arr[start]] -= 1
        start += 1

    print(start,end)
    if remains()<=2:
        ans = max(ans, end-start)

print(ans)
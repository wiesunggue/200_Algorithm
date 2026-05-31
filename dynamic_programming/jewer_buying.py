# https://www.acmicpc.net/problem/2313
# 백준 2313번 보석 구매하기 문제


ans_list = []
def Solution():
    global ans_list
    N = int(input())
    arr = list(map(int,input().split()))

    total = 0
    maxValue = arr[0]
    maxIdx = [(1,1)]
    start,end = 0,0
    while start<N-1:
        print(start,end,total)
        if end == N:
            total -= arr[start]
            start += 1
        elif total >= 0:
            total += arr[end]
            end += 1
        else:
            total -= arr[start]
            total += arr[end]
            start += 1
            end += 1

        if maxValue < total:
            maxValue = total
            maxIdx = [(start+1,end)]
        elif maxValue == total:
            maxIdx.append((start+1,end))

    print(maxIdx,maxValue)
    ans_list.append((sorted(maxIdx,key=lambda arr:(arr[1]-arr[0],arr[0],arr[1]))[0]))
    return maxValue

T = int(input())
value = 0
for t in range(T):
    value += Solution()

print(value)
for x,y in ans_list:
    print(x,y)
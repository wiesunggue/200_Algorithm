# https://www.acmicpc.net/problem/30805
# 백준 사전 순 최대 공통 부분 수열 문제
# 사전순으로 정렬된 LCS를 구하자

N = int(input())
arr1 = list(map(int, input().split()))
M = int(input())
arr2 = list(map(int, input().split()))

# 1 가장 큰 공통 찾기
# 2. 해당 지점부터 가장 큰 공통 찾기
# 3. 해당 지점부터 가장 큰 공통 찾기
x = arr1
y = arr2
i = 0
j = 0
maxLCS = []
intersect = set()
CommonMax = 0
while CommonMax != -1:
    intersect = set(x).intersection(set(y))
    CommonMax = max(intersect,default = -1)
    if CommonMax == -1:
        break
    print(CommonMax)
    i = x.index(CommonMax)
    j = y.index(CommonMax)
    x = x[i+1:]
    y = y[j+1:]
    maxLCS.append(CommonMax)

print(maxLCS)

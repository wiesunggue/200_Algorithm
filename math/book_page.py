# https://www.acmicpc.net/problem/1019
# 책 페이지 문제
from collections import Counter



# 절차
# abcedfg 라고 하면
# 1. 0,1000000,,,,,a0000000 까지 개수 계산
# 2. a* bcdefg 개수 계산
# 3. bcdefg 에대해 계산

def solution(number):
    # 개수 계산하기
    if number < 10:
        arr = [0]*10
        for i in range(1,number+1):
            arr[i] += 1
        return arr

    a = int(str(number)[0])
    last = number - a*10**(len(str(number))-1)
    num = number - last
    # 0~a000 이면 나눠서 계산
    if str(num)[0] == '1':
        arr = solution(num-1)
        arr2 = solution(last)
        for i in range(10):
            arr[i] += arr2[i]
        arr[1] += sum(arr2) + 1
        arr[0] += len(str(num))-1
        return arr

    # a-1000~a000 이면 a:
    l = len(str(num))
    total = 10**(l-1)*l
    second_num = 10**(l-2) * (l-1)
    primary_num = total - second_num * 9

    arr = [0]*10
    arr2 = solution(last)
    arr3 = solution(num//a-1)
    #arr3[1] += 1
    arr3[0] += l-2

    for i in range(10):
        if i==0:
            arr[i] += second_num*(a-1) + arr2[i] + arr3[i]
        elif i <= a:
            arr[i] += primary_num + second_num * (a-2) +arr2[i] + arr3[i]
        else:
            arr[i] += second_num * (a-1) + arr2[i] + arr3[i]
    return arr

def find_pages(num):
    if num <=0:
        return [0] * 10
    if num % 10 != 9:
        print("*****")
        end_with_9 = num-num%10-1
        result = find_pages(end_with_9)
        for i in range(max(0,end_with_9)+1, num+1):
            for n in map(int,list(str(i))):
                result[n] += 1
        print(result,end_with_9,num)
        return result

    arr = [0] * 10
    for i in range(10):
        arr[i] += num//10 + 1
    arr[0] -= 1
    print(num,arr)
    next_num = num//10
    result = find_pages(next_num)
    for i in range(10):
        arr[i] += result[i] * 10
    return arr

data = int(input())

arr = [0]*10
for i in range(1,data+1):
    for t in list(str(i)):
        arr[int(t)] += 1
print(arr)
print(solution(data))
print(find_pages(data))
import sys
sys.setrecursionlimit(10**5)

class NumberOfDifferentNumbers:
    '''
        백준 13547번 수열과 쿼리 5
        Merge Sort Tree를 활용해서 서로 다른 수의 개수 구하기
        
        [풀이] 생각하지도 못한 방식이다.
        주어진 배열을 그대로 사용하는것이 아니고 next[i] 라는 배열을 변경해서 문제를 푼다
        next[i] = i 뒤에서 arr[i] 와 같은 값이 등장하는 첫 번째 위치
        이렇게 하면 [l, r]의 구간 쿼리는 [l, r]에서 next[i]가 r보다 큰 수의 개수 = 서로 다른 수의 개수가 된다.
        이렇게 두고 next[i]에 대해 Merge Sort Tree를 구현하고, 이분탐색으로 next[i] 보다 큰 수의 개수를 세면 된다.
    '''

    
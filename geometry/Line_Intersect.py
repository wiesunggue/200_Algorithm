# https://www.acmicpc.net/problem/17387
# 백준 선분 교차 2 문제

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def sign(x):
    return 0 if x==0 else (-1 if x<0 else 1)

def orient(P,Q,R):
    # R이 선분 PQ 위에 있는지 판변할는 함수
    # 벡터 PR과 PQ의 외적
    val = (Q.x-P.x)*(R.y-P.y) - (Q.y-P.y)*(R.x-P.x) # 외적 연산
    return sign(val)

def included(P,Q,R):
    # PQ위에 한 점이 포함되는 경우
    return min(P.x,Q.x) <= R.x <= max(P.x,Q.x) and \
           min(P.y,Q.y) <= R.y <= max(P.y,Q.y)

def pseudocode(A,B,C,D):
    # 선분 AB와 CD가 교차하는지 판정하기
    o1, o2 = orient(A,B,C), orient(A,B,D)
    o3, o4 = orient(C,D,A), orient(C,D,B)
    if o1 != o2 and o3 != o4:
        return True # 교차하는 경우

    # 특수 케이스: 공평 + 사각형 포함 여부
    if o1==0 and included(A,B,C): return True
    if o2==0 and included(A,B,D): return True
    if o3==0 and included(C,D,A): return True
    if o4==0 and included(C,D,B): return True
    return False

datas = [list(map(int,input().split())) for i in range(2)]
A,B = Point(datas[0][0],datas[0][1]), Point(datas[0][2],datas[0][3])
C,D = Point(datas[1][0],datas[1][1]), Point(datas[1][2],datas[1][3])

print(int(pseudocode(A,B,C,D)))

def solve(A,B,X,Y):
    posX = 0
    posY = 0
    K = 0
    cost = 0
    number = 0

    # 대각선 이동
    if abs(X) < abs(Y):
        # X 방향 이동
        posX, posY = X,+abs(X) if Y > 0 else -abs(X)
        K += abs(X) * 2
        cost += abs(X) * min(A,B) * 2
        # 직선 이동
        number = abs(Y-posY)
        cost += number//2 * (A+B)
        K += (number//2) * 2
        cost += number%2 * (B if K%2==0 else A)
    else:
        posX, posY = abs(Y) if X > 0 else -abs(Y), Y
        K += abs(Y) * 2
        cost += abs(Y) * min(A,B) * 2

        # 직선 이동
        number = abs(X-posX)
        cost += (number//2) * (A+B)
        K += (number//2) * 2
        cost += (number%2) * (A if K%2 == 0 else B)

    print(cost)

T = int(input())

for i in range(T):
    A,B,X,Y = map(int, input().split())
    solve(A,B,X,Y)

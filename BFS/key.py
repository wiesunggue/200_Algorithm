# https://www.acmicpc.net/problem/9328
# 백준 열쇠 문제
from collections import deque, defaultdict
X_pos = [-1,1,0,0]
Y_pos = [0,0,-1,1]

def bfs():
    h, w = map(int,input().split())
    arr = [input() for i in range(h)]

    # 현재 key가 없어서 방문 못한경우 특수 배열에 저장해두자
    need_keys = defaultdict(list)
    keys = set(list(input().upper())+["."])
    dq = deque()
    ans = 0
    # 테두리 부분에서 열쇠 획득 및 문이 존재할 수 있으므로
    # arr 바깥에 사각형으로 .를 추가해서 바깥이면 모두 bfs 절차를 실행하도록 변경
    arr.insert(0,"."*w)
    arr.append("."*w)
    for i in range(len(arr)):
        arr[i] = "."+arr[i]+"."

    h, w = h+2, w+2
    visited = [[0]*w for i in range(h)]

    # 0,0 에서 bfs 시작
    dq.append((0,0))
    visited[0][0] = 1

    while dq:
        x,y = dq.popleft()
        for i in range(4):
            new_x,new_y = x+X_pos[i], y+Y_pos[i]
            if 0 <= new_x < h and 0<= new_y < w and arr[new_x][new_y] != "*" and visited[new_x][new_y]==0:

                # 문을 만나는 경우를 제외하면 모두 deque에 넣어야 함
                visited[new_x][new_y] = 1

                # 문서가 있는 경우
                if arr[new_x][new_y] == '$':
                    ans += 1
                    dq.append((new_x,new_y))

                # 문을 만났는데 key에 있는 경우 or 문이 없는 경우
                elif arr[new_x][new_y] in keys:
                    dq.append((new_x,new_y))

                # key를 획득하는 경우
                elif 'a' <= arr[new_x][new_y] <= 'z':
                    dq.append((new_x,new_y))
                    keys.add(arr[new_x][new_y].upper())
                    if need_keys.get(arr[new_x][new_y].upper()) is not None:
                        dq.extend(need_keys[arr[new_x][new_y].upper()])
                        need_keys.pop(arr[new_x][new_y].upper())

                # 문을 만났고 key가 없는 경우
                else:
                    need_keys[arr[new_x][new_y].upper()].append((new_x,new_y))
    return ans

T = int(input())
for test in range(T):
    print(bfs())


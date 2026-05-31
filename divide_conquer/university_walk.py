# https://www.acmicpc.net/problem/12850
# 백준 본대 산책 문제
MAX_VAL = 1000000007
matrix = [[0,1,1,0,0,0,0,0],
          [1,0,1,1,0,0,0,0],
          [1,1,0,1,0,1,0,0],
          [0,1,1,0,1,1,0,0],
          [0,0,0,1,0,1,1,0],
          [0,0,1,1,1,0,0,1],
          [0,0,0,0,1,0,0,1],
          [0,0,0,0,0,1,1,0]]
idx = 0
hashMatrix = [[[-1 for k in range(8)]for j in range(8)] for i in range(10000)]
MatrixDict = {}

def NumberOfCase(start, end, size):
    # 경우의 수 계산 함수
    global idx
    data = 0
    # 엣지 케이스
    if size == 0:
        return 1 if start==end else 0
    if size == 1:
        return matrix[start][end]
    if MatrixDict.get(size) != None and hashMatrix[MatrixDict[size]][start][end] != -1:
        return hashMatrix[MatrixDict[size]][start][end]
    for i in range(8):
        data += NumberOfCase(start,i,size//2) * NumberOfCase(i,end,size-size//2)
        data %= MAX_VAL

    if MatrixDict.get(size) == None:
        MatrixDict[size] = idx
        idx += 1
    hashMatrix[MatrixDict[size]][start][end] = data
    return data

print(NumberOfCase(0,0,100000000))
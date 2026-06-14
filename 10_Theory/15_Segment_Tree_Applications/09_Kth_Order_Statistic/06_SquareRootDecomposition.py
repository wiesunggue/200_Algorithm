import bisect
'''
파이썬에서는 Block의 사이즈를 sqrt(N) 대신 500~1000사이 숫자를 사용하기도 한다.

'''
class SqrtDecomposition:
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr

        self.B = int(self.N ** 0.5) + 1

        self.num_blocks = (self.N + self.B - 1) // self.B
        self.block_sum = [0] * self.num_blocks

        for i, value in enumerate(self.arr):
            b = i // self.B
            self.block_sum[b] += value

    def update(self, idx, value):
        b = idx // self.B

        self.block_sum[b] -= self.arr[idx]
        self.arr[idx] = value
        self.block_sum[b] += value
    
    def query(self, left, right):
        result = 0
        
        start_block = left // self.B
        end_block = right // self.B

        if start_block == end_block:
            for i in range(left, right + 1):
                result += self.arr[i]
            return result
        
        left_end = (start_block + 1) * self.B -1
        for i in range(left, min(left_end, self.N-1)+1):
            result += self.arr[i]

        for b in range(start_block + 1, end_block):
            result += self.block_sum[b]
        
        right_start = end_block * self.B
        for i in range(right_start, right + 1):
            result += self.arr[i]
        
        return result
    

class KthSqrtDecomposition:
    '''K 이하인 개수 찾기 알고리즘'''
    def __init__(self, arr):
        self.N = len(arr)
        self.arr = arr

        self.B = int(self.N ** 0.5) + 1

        self.num_blocks = (self.N + self.B - 1) // self.B
        self.block = [[] for i in range(self.num_blocks)]

        for i in range(self.num_blocks):
            self.block[i] = sorted(self.arr[self.B*i : self.B*(i + 1)])

    
    def update(self, idx, value):
        before = self.arr[idx]
        b = idx // self.B
        self.arr[idx] = value
        self.block[b] = self.arr[self.B*b : self.B*(b + 1)]
        self.block[b].sort()

    def query(self, left, right, x):
        '''구간 [left, right]에서 x이하인 개수'''
        result = 0

        start_block = left//self.B
        end_block = right//self.B

        if start_block == end_block:
            for i in range(left, right + 1):
                result += 1 if self.arr[i] <= x else 0
                return result
        
        left_end = (start_block + 1) * self.B - 1        
        for i in range(left, min(left_end, self.N - 1) + 1):
            result += 1 if self.arr[i] <= x else 0
        
        for b in range(start_block + 1, end_block):
            result += bisect.bisect_right(self.block[b], x)

        right_start = end_block * self.B
        for i in range(right_start, right + 1):
            result += 1 if self.arr[i] <= x else 0

        return result
        
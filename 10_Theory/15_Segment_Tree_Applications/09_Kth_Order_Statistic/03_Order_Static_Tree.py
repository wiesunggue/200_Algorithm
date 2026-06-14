'''
    C++에는 기본 컨테이너로 지원함
    PBDS라고 부름
    Bineary Search Tree + 노드의 개수를 저장하여 통계 연산 압축 진행
    해당 예제는 균현잡히지 않은 구조라서 필요 메모리 사이즈가 극단적으로 커질 수 있음
'''

class BST:
    '''BST + SubTree의 노드 개수 저장하는 구조'''
    def __init__(self,N):
        self.N = N
        self.arr = [0] * (N+1)
        self.sub_size = [0] * (N+1)

    def insert(self,value):
        start = 1
        while self.sub_size[start] != 0:
            self.sub_size[start] += 1
            if self.arr[start] < value:
                start = start * 2 + 1
            else:
                start = start * 2
        self.sub_size[start] += 1
        self.arr[start] = value

    def erase(self, ):
        pass

    def kth_find(self, k):
        '''K 번째 수를 찾기'''
        start = 1

        while start < self.N:
            left = start * 2
            right = start * 2 + 1
            if k <= self.sub_size[left]:
                start = left
            elif k == self.sub_size[left] + 1:
                return self.arr[start]
            else:
                k -= self.sub_size[left] + 1
                start = right

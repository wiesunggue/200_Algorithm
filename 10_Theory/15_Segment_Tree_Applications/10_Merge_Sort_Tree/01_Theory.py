
'''
    대표적인 예제
    1. K 번째 수 구하기
    2. 구간에서 서로 다른 수의 개수 구하기
    3. 구간 과반수 구하기 - 과반수 이상 등장하는 수 찾아서 반환하기
    4. 직사각형 안에 들어가는 점의 개수 구하기
    5. 구간 안에 완전히 포함되는 구간의 개수 구하기
    6. Top - K 합
    7. 동적 Merge Sort Tree에서 K보다 큰 원소의 개수 구하기
'''

class MergeSortTree:
    '''
        Merge Sort Tree
        노드에 배열을 저장하는 세그먼트 트리
        구간 A,B를 선택하면 항상 해당 배열은 정렬된 상태를 유지해야 한다.
    '''
    def __init__(self, arr):
        self.arr = arr
        self.N = len(arr)
        self.size = 1

        while self.size < self.N:
            self.size *= 2

        self.tree = [[] for i in range(self.size * 2)]

        self._build(1, 0, self.N-1)
    
    def _build(self, node, left, right):
        if left == right:
            self.tree[node].append(self.arr[left])
            return self.tree[node]
        
        mid = (left + right) // 2
        self.tree[node] = self._merge(self._build(node * 2, left, mid), self._build(node * 2 + 1, mid + 1, right))
        return self.tree[node]
    
    def _query(self, node, left, right, l, r):
        if right < l or r < left:
            return []
        
        if l <= left and right <= r:
            return self.tree[node]
        
        mid = (left + right) // 2
        return self._merge(self._query(node * 2, left, mid, l, r),self._query(node * 2 + 1, mid + 1, right, l, r))

    def _merge(self, arr1, arr2):
        arr = []
        n1, n2 = 0, 0
        while n1 < len(arr1) and n2 < len(arr2):
            if arr1[n1] <= arr2[n2]:
                arr.append(arr1[n1])
                n1 += 1
            else:
                arr.append(arr2[n2])
                n2 += 1
        
        while n1 < len(arr1):
            arr.append(arr1[n1])
            n1 += 1

        while n2 < len(arr2):
            arr.append(arr2[n2])
            n2 += 1
        
        return arr
            
    def query(self, l, r):
        return self._query(1,0,self.N-1, l, r)
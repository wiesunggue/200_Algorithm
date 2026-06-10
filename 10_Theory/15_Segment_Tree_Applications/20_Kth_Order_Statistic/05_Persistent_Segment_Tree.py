'''
Persistent Segment Tree
세그먼트 트리 중 업데이트 가능하고 히스토리 관리가 가능한 트리의 일종
'''

class PersistentSegmentTree:
    """
    Point Add + Range Sum Persistent Segment Tree

    값의 범위: [0, n - 1]
    root 0번은 아무 값도 없는 빈 세그먼트 트리
    """

    def __init__(self, n):
        self.n = n

        # 0번 노드는 null node
        self.left = [0]
        self.right = [0]
        self.sum = [0]

        # roots[i] = i번째 버전의 root
        self.roots = [0]

    def _clone(self, node):
        """
        기존 node를 복사해서 새 노드를 만든다.
        Python에서는 Node 객체보다 배열 풀 방식이 빠르고 메모리도 안정적이다.
        """
        self.left.append(self.left[node])
        self.right.append(self.right[node])
        self.sum.append(self.sum[node])
        return len(self.sum) - 1

    def add(self, prev_root, idx, delta=1):
        """
        prev_root 버전에서 idx 위치에 delta를 더한 새 root를 반환한다.
        """
        return self._add(prev_root, 0, self.n - 1, idx, delta)

    def _add(self, prev_node, node_left, node_right, idx, delta):
        # 현재 노드는 이전 노드를 복사해서 만든다.
        cur = self._clone(prev_node)

        # 현재 구간 전체 합에 delta 반영
        self.sum[cur] += delta

        if node_left == node_right:
            return cur

        mid = (node_left + node_right) // 2

        if idx <= mid:
            # 왼쪽 자식만 새로 만든다.
            self.left[cur] = self._add(
                self.left[prev_node],
                node_left,
                mid,
                idx,
                delta
            )
        else:
            # 오른쪽 자식만 새로 만든다.
            self.right[cur] = self._add(
                self.right[prev_node],
                mid + 1,
                node_right,
                idx,
                delta
            )

        return cur

    def append_version(self, idx, delta=1):
        """
        마지막 버전에서 idx 위치에 delta를 더한 새 버전을 roots에 추가한다.
        """
        new_root = self.add(self.roots[-1], idx, delta)
        self.roots.append(new_root)
        return new_root

    def query_sum(self, root, ql, qr):
        """
        root 버전에서 [ql, qr] 구간 합을 구한다.
        """
        return self._query_sum(root, 0, self.n - 1, ql, qr)

    def _query_sum(self, node, node_left, node_right, ql, qr):
        if node == 0:
            return 0

        if qr < node_left or node_right < ql:
            return 0

        if ql <= node_left and node_right <= qr:
            return self.sum[node]

        mid = (node_left + node_right) // 2

        return (
            self._query_sum(self.left[node], node_left, mid, ql, qr)
            + self._query_sum(self.right[node], mid + 1, node_right, ql, qr)
        )
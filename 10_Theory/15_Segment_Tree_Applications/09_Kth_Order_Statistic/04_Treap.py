'''
    Treap 구현하기
    Treap의 핵심 연산
    Insert 값 삽입하기
    Erease 값 삭제하기
    Split(root, key) 트립을 두 개의 트립으로 분리하기
    Merge(left, right) 두 트립을 합치기
    Rank 정렬 순서에서 몇 번째인지 구하기
'''

class Node:
    __slots__ = ('key', 'priority', 'count', 'size', 'left', 'right')

def size(node):
    return node.size if node else 0

def update(node : Node):
    if node:
        node.size = node.count + size(node.left) + size(node.right)

def split(root : Node, key):
    if root is None:
        return None, None
    
    if root.key < key:
        left_sub, right_sub = split(root.right, key)
        root.right = left_sub
        update(root)
        return root, right_sub
    else:
        left_sub, right_sub = split(root.left, key)
        root.left = right_sub
        update(root)
        return left_sub, root
    
def merge(left : Node, right : Node):
    if left is None:
        return right
    
    if right is None:
        return left
    
    if left.priority < right.priority:
        left.right = merge(left.right, right)
        update(left)
        return left
    else:
        right.left = merge(left, right.left)
        update(right)
        return right
    

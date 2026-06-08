'''
    Quick Select 알고리즘
'''
import random

def quick_select(arr, k):
    left, right = 0, len(arr) - 1

    while left <= right:
        pivot_index = random.randint(left, right)
        pivot_index = partition(arr, left, right, pivot_index)

        if pivot_index == k:
            return arr[pivot_index]
        
        if k < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1
    

def partition(arr, left, right, pivot_index):
    
    pivot = arr[pivot_index]
    stored = left

    arr[pivot_index], arr[right] = arr[right], arr[pivot_index]

    for i in range(left, right):
        if arr[i] < pivot:
            arr[stored], arr[i] = arr[i], arr[stored]
            stored += 1

    
    arr[right], arr[stored] = arr[stored], arr[right]

    return stored

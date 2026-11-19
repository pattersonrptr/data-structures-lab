def insert_search(nums, target):
    return binary_search(nums,target, 0, len(nums) - 1)

def recursive_binary_search(nums, target, left, right):
    if left > right:
        return left
    
    mid = (left + right) // 2

    if nums[mid] == target:
        return mid

    if nums[mid] > target:
        return recursive_binary_search(nums, target, left, mid - 1)
    else:
        return recursive_binary_search(nums, target, mid + 1, right)

def binary_search(nums, target, left, right):
    while left <= right:
        mid = (left + right) // 2
    
        if nums[mid] == target:
            return mid

        if nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1

    return left


if __name__ == "__main__":
    nums = [0, 1, 3, 4, 5, 7, 9, 11, 12, 13, 15]
    target = 13

    found = insert_search(nums, target)

    print(found)

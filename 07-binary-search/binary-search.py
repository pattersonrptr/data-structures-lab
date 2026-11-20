def insert_search(nums, target):
    return binary_search(nums, target, 0, len(nums) - 1)

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
        # Python ints do not overflow. In Java/C, use left + (right - left) // 2.
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        if nums[mid] > target:
            right = mid - 1
        else:
            left = mid + 1

    return left


def first_occurrence(nums, target):
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            result = mid
            right = mid - 1  # keep looking for an earlier copy
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def last_occurrence(nums, target):
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            result = mid
            left = mid + 1  # keep looking for a later copy
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


def rotated_search(nums, target):
    # Assumes distinct values.
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid

        # At least one half is sorted; check whether the target is inside it.
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1

    return -1


def search_both(nums, target):
    iterative = insert_search(nums, target)
    recursive = recursive_binary_search(nums, target, 0, len(nums) - 1)
    assert iterative == recursive
    return iterative


def test_finds_every_value():
    nums = [0, 1, 3, 4, 5, 7, 9, 11, 12, 13, 15]

    for index, value in enumerate(nums):
        assert search_both(nums, value) == index


def test_empty_list():
    assert search_both([], 5) == 0


def test_target_smaller_than_all():
    assert search_both([3, 5, 7], 1) == 0


def test_target_larger_than_all():
    assert search_both([3, 5, 7], 9) == 3


def test_single_element():
    assert search_both([5], 5) == 0
    assert search_both([5], 1) == 0
    assert search_both([5], 9) == 1


def test_missing_target_in_the_middle_returns_insert_position():
    nums = [1, 3, 5, 7]

    assert search_both(nums, 2) == 1
    assert search_both(nums, 4) == 2
    assert search_both(nums, 6) == 3


def test_first_and_last_occurrence():
    nums = [1, 2, 2, 2, 3, 5, 5]

    assert first_occurrence(nums, 2) == 1
    assert last_occurrence(nums, 2) == 3
    assert first_occurrence(nums, 5) == 5
    assert last_occurrence(nums, 5) == 6
    assert first_occurrence(nums, 1) == 0
    assert last_occurrence(nums, 1) == 0


def test_first_and_last_occurrence_edge_cases():
    assert first_occurrence([], 1) == -1
    assert last_occurrence([], 1) == -1
    assert first_occurrence([1, 3, 5], 4) == -1
    assert last_occurrence([1, 3, 5], 4) == -1
    assert first_occurrence([7, 7, 7], 7) == 0
    assert last_occurrence([7, 7, 7], 7) == 2


def test_rotated_search():
    nums = [4, 5, 6, 7, 0, 1, 2]

    for index, value in enumerate(nums):
        assert rotated_search(nums, value) == index
    assert rotated_search(nums, 3) == -1
    assert rotated_search(nums, 8) == -1


def test_rotated_search_on_every_rotation():
    base = [1, 2, 3, 4, 5, 6, 7]

    for k in range(len(base)):
        nums = base[k:] + base[:k]

        for index, value in enumerate(nums):
            assert rotated_search(nums, value) == index
        assert rotated_search(nums, 0) == -1
        assert rotated_search(nums, 8) == -1


def test_rotated_search_edge_cases():
    assert rotated_search([], 1) == -1
    assert rotated_search([1], 1) == 0
    assert rotated_search([1], 2) == -1
    assert rotated_search([2, 1], 1) == 1
    assert rotated_search([2, 1], 2) == 0


if __name__ == "__main__":
    tests = [
        test_finds_every_value,
        test_empty_list,
        test_target_smaller_than_all,
        test_target_larger_than_all,
        test_single_element,
        test_missing_target_in_the_middle_returns_insert_position,
        test_first_and_last_occurrence,
        test_first_and_last_occurrence_edge_cases,
        test_rotated_search,
        test_rotated_search_on_every_rotation,
        test_rotated_search_edge_cases,
    ]

    for test in tests:
        test()
        print("ok:", test.__name__)

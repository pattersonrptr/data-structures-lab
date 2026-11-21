import random


# ---------- version 1: new lists on every call (stable, O(n) extra memory on average) ----------

def quick_sort_lists(nums):
    """Return a new sorted list. Stable, because the comprehensions keep the original order."""
    return _quick_lists(list(nums))  # copy once here, not on every recursive call


def _quick_lists(nums):
    if len(nums) <= 1:
        return nums

    # Random pivot: no fixed input is bad anymore. Worst case is still O(n²), just very unlikely.
    pivot = random.choice(nums)
    lt = [x for x in nums if x < pivot]
    gt = [x for x in nums if pivot < x]
    eq = [x for x in nums if not x < pivot and not pivot < x]  # only `<`, like sorted()

    return _quick_lists(lt) + eq + _quick_lists(gt)


# ---------- version 2: classic in-place, Hoare partition (not stable, O(log n) stack on average) ----------

def quick_sort(nums):
    """Return a new sorted list. Not stable: long-distance swaps can reorder equal keys."""
    result = list(nums)  # copy: we sort in place, so the caller's list stays intact
    _quick(result, 0, len(result) - 1)
    return result


def _quick(nums, lo, hi):
    """Sort nums[lo..hi] in place (hi is inclusive)."""
    if lo >= hi:
        return

    p = _partition(nums, lo, hi)
    _quick(nums, lo, p)
    _quick(nums, p + 1, hi)


def _partition(nums, lo, hi):
    """
    Hoare partition. Returns p such that every element of nums[lo..p] <= every element of nums[p+1..hi].
    The pivot does not necessarily end up at p, that is why we recurse on [lo..p] and not [lo..p-1].
    """
    # Move a random pivot to lo. With the pivot at lo, j never returns hi,
    # so both sides are always smaller than the input (no infinite recursion on e.g. [1, 2]).
    r = random.randint(lo, hi)
    nums[lo], nums[r] = nums[r], nums[lo]
    pivot = nums[lo]

    i, j = lo - 1, hi + 1
    while True:
        # Both stop on elements EQUAL to the pivot: that keeps the split balanced on many duplicates.
        i += 1
        while nums[i] < pivot:
            i += 1

        j -= 1
        while pivot < nums[j]:
            j -= 1

        if i >= j:
            return j

        nums[i], nums[j] = nums[j], nums[i]


# ---------- tests ----------

SORTS = [quick_sort_lists, quick_sort]


class Item:
    """Compares only by key, so we can see whether equal keys keep their order."""

    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __lt__(self, other):
        return self.key < other.key


def middle_pivot_killer(n):
    """Input where the middle element is always the largest left: O(n²) for a fixed middle pivot."""
    positions, nums, value = list(range(n)), [0] * n, n
    while positions:
        nums[positions.pop(len(positions) // 2)] = value
        value -= 1
    return nums


def test_empty_list():
    for sort in SORTS:
        assert sort([]) == []


def test_single_element():
    for sort in SORTS:
        assert sort([5]) == [5]


def test_two_elements():
    for sort in SORTS:
        assert sort([2, 1]) == [1, 2]
        assert sort([1, 2]) == [1, 2]


def test_already_sorted():
    for sort in SORTS:
        assert sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    for sort in SORTS:
        assert sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_duplicates():
    for sort in SORTS:
        assert sort([3, 1, 3, 2, 1, 3]) == [1, 1, 2, 3, 3, 3]


def test_all_equal():
    for sort in SORTS:
        assert sort([7] * 1000) == [7] * 1000


def test_negative_numbers():
    for sort in SORTS:
        assert sort([0, -3, 5, -1]) == [-3, -1, 0, 5]


def test_returns_new_list_and_keeps_input_intact():
    for sort in SORTS:
        for nums in ([], [5], [3, 1, 2]):
            original = list(nums)
            result = sort(nums)
            assert result is not nums
            assert nums == original


def test_middle_pivot_killer_does_not_hit_recursion_limit():
    nums = middle_pivot_killer(3000)  # the old version raised RecursionError here
    for sort in SORTS:
        assert sort(nums) == list(range(1, 3001))


def test_large_sorted_input():
    nums = list(range(3000))
    for sort in SORTS:
        assert sort(nums) == nums


def test_lists_version_is_stable():
    items = [Item(25, "Ana"), Item(30, "Bia"), Item(25, "Caio"), Item(20, "Dan"), Item(30, "Eva")]
    labels = [item.label for item in quick_sort_lists(items)]
    assert labels == ["Dan", "Ana", "Caio", "Bia", "Eva"]


def test_matches_builtin_sorted_on_random_lists():
    for sort in SORTS:
        for size in range(50):
            nums = [random.randint(-10, 10) for _ in range(size)]
            assert sort(nums) == sorted(nums)


if __name__ == "__main__":
    tests = [
        test_empty_list,
        test_single_element,
        test_two_elements,
        test_already_sorted,
        test_reverse_sorted,
        test_duplicates,
        test_all_equal,
        test_negative_numbers,
        test_returns_new_list_and_keeps_input_intact,
        test_middle_pivot_killer_does_not_hit_recursion_limit,
        test_large_sorted_input,
        test_lists_version_is_stable,
        test_matches_builtin_sorted_on_random_lists,
    ]

    for test in tests:
        test()

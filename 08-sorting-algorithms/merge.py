import random


def merge_sort(nums):
    """Return a new sorted list. Stable. O(n log n) time, O(n) extra memory."""
    result = list(nums)  # copy: we sort in place, so the caller's list stays intact (also accepts any iterable)
    buffer = [None] * len(result)  # allocated once, reused by every merge
    _sort(result, buffer, 0, len(result))
    return result


def _sort(nums, buffer, lo, hi):
    """Sort nums[lo:hi] in place (hi is exclusive)."""
    if hi - lo < 2:
        return

    mid = (lo + hi) // 2
    _sort(nums, buffer, lo, mid)
    _sort(nums, buffer, mid, hi)

    # Halves already in order (last of left <= first of right): nothing to merge.
    # Makes already sorted input O(n): T(n) = 2T(n/2) + O(1).
    if not nums[mid] < nums[mid - 1]:
        return

    _merge(nums, buffer, lo, mid, hi)


def _merge(nums, buffer, lo, mid, hi):
    """Merge the sorted runs nums[lo:mid] and nums[mid:hi] back into nums[lo:hi]."""
    for k in range(lo, hi):
        buffer[k] = nums[k]

    i, j = lo, mid
    for k in range(lo, hi):
        # Take from the right only when it is strictly smaller:
        # on ties the left element goes first, which keeps the sort stable.
        if i < mid and (j >= hi or not buffer[j] < buffer[i]):
            nums[k] = buffer[i]
            i += 1
        else:
            nums[k] = buffer[j]
            j += 1


# ---------- tests ----------

class Item:
    """Compares only by key, so we can see whether equal keys keep their order."""

    def __init__(self, key, label):
        self.key = key
        self.label = label

    def __lt__(self, other):
        return self.key < other.key


class Counted:
    """Counts every comparison, to check how much work the sort does."""

    comparisons = 0

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        Counted.comparisons += 1
        return self.value < other.value


def test_empty_list():
    assert merge_sort([]) == []


def test_single_element():
    assert merge_sort([5]) == [5]


def test_two_elements():
    assert merge_sort([2, 1]) == [1, 2]
    assert merge_sort([1, 2]) == [1, 2]


def test_already_sorted():
    assert merge_sort([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]


def test_reverse_sorted():
    assert merge_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_duplicates():
    assert merge_sort([3, 1, 3, 2, 1, 3]) == [1, 1, 2, 3, 3, 3]
    assert merge_sort([7, 7, 7]) == [7, 7, 7]


def test_negative_numbers():
    assert merge_sort([0, -3, 5, -1]) == [-3, -1, 0, 5]


def test_returns_new_list_and_keeps_input_intact():
    for nums in ([], [5], [3, 1, 2]):
        original = list(nums)
        result = merge_sort(nums)
        assert result is not nums
        assert nums == original


def test_is_stable():
    items = [Item(25, "Ana"), Item(30, "Bia"), Item(25, "Caio"), Item(20, "Dan"), Item(30, "Eva")]
    labels = [item.label for item in merge_sort(items)]
    assert labels == ["Dan", "Ana", "Caio", "Bia", "Eva"]


def test_sorted_input_skips_every_merge():
    # Each of the n - 1 internal calls does exactly one check and no merge.
    for n in (1, 2, 7, 100, 1000):
        Counted.comparisons = 0
        merge_sort([Counted(x) for x in range(n)])
        assert Counted.comparisons == max(n - 1, 0)


def test_matches_builtin_sorted_on_random_lists():
    for size in range(50):
        nums = [random.randint(-10, 10) for _ in range(size)]
        assert merge_sort(nums) == sorted(nums)


if __name__ == "__main__":
    tests = [
        test_empty_list,
        test_single_element,
        test_two_elements,
        test_already_sorted,
        test_reverse_sorted,
        test_duplicates,
        test_negative_numbers,
        test_returns_new_list_and_keeps_input_intact,
        test_is_stable,
        test_sorted_input_skips_every_merge,
        test_matches_builtin_sorted_on_random_lists,
    ]

    for test in tests:
        test()

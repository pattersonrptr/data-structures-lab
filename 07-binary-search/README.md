# 07 - Binary search

Finding a value in a **sorted** array by repeatedly halving the search range. Guiding questions: why does halving the range give O(log n)? What should the search return when the target is not in the array? Why do the bounds (`left <= right`, `mid - 1`, `mid + 1`) cause so many off-by-one bugs?

- [x] Iterative binary search
- [x] Recursive binary search
- [x] Insert position (returns the index where the target would be inserted)
- [x] Lower bound and upper bound (first and last occurrence with duplicates)
- [x] Search in a rotated sorted array
- [ ] Binary search on the answer (e.g. smallest value that satisfies a condition)

## Complexity

| Version | Time | Space | Why |
|---------|------|-------|-----|
| Iterative | O(log n) | O(1) | Each step discards half of the remaining range, so at most log2(n) steps. |
| Recursive | O(log n) | O(log n) | Same steps, but each call stays on the stack until the search ends. |
| First / last occurrence | O(log n) | O(1) | Same halving; a match only narrows the range instead of stopping. |
| Rotated array | O(log n) | O(1) | Same halving; one extra comparison picks the sorted half. |

## Insert position

When the target is missing, the loop ends with `left > right`, and `left` is exactly the index where the target would keep the array sorted. That is why both versions return `left` instead of `-1`: the same code answers "where is it?" and "where should it go?".

## First and last occurrence

With duplicates, the basic search stops at whichever copy `mid` hits first. To find the first copy, a match is saved as a candidate and the search continues to the left (`right = mid - 1`); for the last copy, it continues to the right (`left = mid + 1`). When the loop ends, the last saved candidate is the answer, or `-1` if there was no match.

## Rotated sorted array

A sorted array rotated at some point, such as `[4, 5, 6, 7, 0, 1, 2]`. It is not sorted as a whole, but at any `mid` at least one half is: if `nums[left] <= nums[mid]`, the left half is sorted; otherwise the right half is. Inside the sorted half, comparing the target with both ends tells for sure whether it is there, so the search goes to that half or to the other one. This assumes distinct values: with duplicates, `nums[left] == nums[mid]` does not tell which half is sorted, and the worst case becomes O(n).

## Overflow in `mid`

In Java or C, `int` has a fixed size (32 bits, up to about 2.1 billion). On a huge array, `left + right` can go past that limit and wrap around to a negative number, giving an invalid index. `left + (right - left) / 2` computes the same value without adding two large numbers: `right - left` always fits, and adding half of it to `left` never goes past `right`. Python integers have no fixed size, so `(left + right) // 2` is safe here.

## Files

- [binary-search.py](binary-search.py): iterative and recursive versions, first and last occurrence, rotated search, and `test_*` functions with `assert`. Running the file executes all of them and prints `ok:` for each one that passes.

# 07 - Binary search

Finding a value in a **sorted** array by repeatedly halving the search range. Guiding questions: why does halving the range give O(log n)? What should the search return when the target is not in the array? Why do the bounds (`left <= right`, `mid - 1`, `mid + 1`) cause so many off-by-one bugs?

- [x] Iterative binary search
- [x] Recursive binary search
- [x] Insert position (returns the index where the target would be inserted)
- [ ] Lower bound and upper bound (first and last occurrence with duplicates)
- [ ] Binary search on the answer (e.g. smallest value that satisfies a condition)

## Complexity

| Version | Time | Space | Why |
|---------|------|-------|-----|
| Iterative | O(log n) | O(1) | Each step discards half of the remaining range, so at most log2(n) steps. |
| Recursive | O(log n) | O(log n) | Same steps, but each call stays on the stack until the search ends. |

## Insert position

When the target is missing, the loop ends with `left > right`, and `left` is exactly the index where the target would keep the array sorted. That is why both versions return `left` instead of `-1`: the same code answers "where is it?" and "where should it go?".

## Files

- [bynary-search.py](bynary-search.py): iterative and recursive versions, plus a small example in `__main__`.

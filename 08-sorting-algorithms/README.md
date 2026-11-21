# 08 - Sorting algorithms

Two divide-and-conquer sorts: merge sort and quick sort. Guiding questions: why do both reach O(n log n), and why can quick sort still fall to O(n²)? What does "stable" mean, and which of them is? Why is the one with more comparisons faster in practice?

- [x] Merge sort with indices and a single buffer (stable)
- [x] Merge sort skips the merge when both halves are already in order (sorted input in O(n))
- [x] Quick sort with new lists on every call (stable, random pivot)
- [x] Quick sort in place with Hoare partition (not stable, random pivot)
- [ ] Quickselect (k-th smallest value in O(n) on average)

## Complexity

| Version | Best | Average | Worst | Extra space | Stable |
|---------|------|---------|-------|-------------|--------|
| `merge_sort` | O(n) | O(n log n) | O(n log n) | O(n) | yes |
| `quick_sort_lists` | O(n log n) | O(n log n) | O(n²) | O(n) average, O(n²) worst | yes |
| `quick_sort` (Hoare) | O(n log n) | O(n log n) | O(n²) | O(log n) average, O(n) worst | no |

- **Merge sort** always splits in half, so there are log2(n) levels, and each level moves all n elements once. The best case is O(n) only because of the skip check: on sorted input every call does one comparison and no merge.
- **Quick sort** is O(n log n) when the pivot splits the range into two parts of similar size. When the pivot is the smallest or largest value, one side gets n - 1 elements, the recursion goes n levels deep, and the work becomes n + (n - 1) + ... = O(n²).
- **Extra space** does not count the copy of the input that every public function makes to return a new list.

## Merge sort

Implementation: [merge.py](merge.py). Split the range in half, sort each half, then merge the two sorted halves into one.

**Why the base case is enough.** A list with 0 or 1 elements is already sorted. Each merge of two sorted lists gives a sorted list, so by induction the result is sorted all the way up. Stopping at size 1 is also necessary: with one element, `mid` is 0 and one half would be the same list again, so the recursion would never end.

**Stability.** On a tie, the merge takes the element from the **left** half first. Equal keys keep their original order, which matters when sorting by several criteria (for example by name, then by age). Taking from the right on ties would still sort, but would no longer be stable. The code writes the tie rule as `not buffer[j] < buffer[i]`, so it only needs `<`, like `sorted()`.

**Indices and one buffer instead of slices.** The first version created new lists with `nums[:mid]` and `nums[mid:]` on every call. Each level copies n elements in total, so the time stays O(n log n), but the program allocates O(n log n) memory over the whole run. The current version passes `lo` and `hi` and reuses one buffer created once, so it allocates O(n) in total. In CPython this is **not faster**: slices and `extend` run in C, while the buffer copies are Python loops. It is the model you would write in C or Java.

**Skipping the merge.** If the last element of the left half is not greater than the first of the right half, the two halves together are already in order. On sorted input every call skips its merge, which gives T(n) = 2T(n/2) + O(1) = O(n). A test checks this by counting exactly n - 1 comparisons. On random input the check almost never helps and costs one comparison per call.

## Quick sort

Implementation: [quick.py](quick.py). Choose a pivot, put smaller elements on the left and larger ones on the right, then sort each side.

**Choosing the pivot.** A pivot in the middle position protects only against sorted or reversed input, where the middle position happens to hold the median value. Position is not value: `middle_pivot_killer` builds an input where the middle element is always the largest left, and the old middle-pivot version raised `RecursionError` on it with 3000 elements. A random pivot means no fixed input is bad. The worst case still exists, but its probability is negligible.

**Two versions.**

- `quick_sort_lists` builds three new lists per call (`lt`, `eq`, `gt`). The comprehensions keep the original order, so it is stable. The `eq` list also means an input with all values equal ends in one level. While `_quick_lists(lt)` runs, the caller still holds its lists, so the extra memory is O(n) on average and O(n²) in the worst case.
- `quick_sort` partitions in place with the Hoare scheme: `i` moves from the left and `j` from the right, each stopping at an element on the wrong side, and the two are swapped. The only extra memory is the recursion stack. Long-distance swaps can reorder equal keys, so it is not stable.

**Hoare details that matter.**

- Both indices stop on elements **equal** to the pivot. That looks like wasted swaps, but it makes them meet in the middle on many duplicates. If they skipped equal elements, one index would run to the end and the split would be n - 1 against 1.
- The random pivot is moved to `lo` before partitioning. With the pivot at `hi`, an input such as `[1, 2]` makes the partition return `hi`, and the recursion calls the same range forever.
- The recursion uses `[lo..p]` and `[p+1..hi]`, not `p - 1`, because in Hoare the pivot does not necessarily end at position `p`.

## Measurements

One million random integers, CPython, best of 3 runs:

| Version | Time | Peak extra memory |
|---------|------|-------------------|
| `quick_sort` (Hoare) | 3.3 s | ~8 MB (only the copy of the input) |
| `quick_sort_lists` | 4.2 s | ~44 MB |
| `merge_sort` | 5.2 s | ~15 MB (copy + buffer) |
| `sorted()` | 0.26 s | ~11 MB |

Comparisons counted on 100 000 elements:

| Version | Random | Nearly sorted (100 swaps) |
|---------|--------|---------------------------|
| `quick_sort` (Hoare) | 2.36 M | 2.44 M |
| `merge_sort` (before the skip check) | 1.54 M | 1.02 M |
| `sorted()` | 1.53 M | 0.10 M |

- Quick sort makes about 50% more comparisons than merge sort (theory: about 1.39 n log2 n against n log2 n) and is still faster. Comparing integers is cheap; moving data is not, and merge sort copies everything to the buffer and back on every level.
- In Python, comparing objects calls `__lt__`, which is expensive. That is one reason Python chose a merge-based sort (Timsort) for `sorted()`: fewer comparisons, and stable.
- On random input `sorted()` makes the same number of comparisons as our merge sort; its advantage there is being written in C. On nearly sorted input it makes about n comparisons, because it detects the runs that are already in order. That advantage is in the algorithm.

## When to use each

| Scenario | Better | Why |
|----------|--------|-----|
| Array in memory, stability not needed | Quick | In place, cache friendly, faster in practice. |
| Must be stable (several criteria) | Merge | In-place quick sort reorders equal keys. |
| Guaranteed worst case (hostile input, real time) | Merge | O(n log n) for every input. |
| Little extra memory | Quick | O(log n) stack against an O(n) buffer. |
| Nearly sorted data | Adaptive merge / Timsort | Takes advantage of the parts already in order. |
| Data larger than RAM | Merge (external) | Sort chunks that fit in memory, then merge the k sorted runs reading sequentially, with a min-heap to pick the smallest head. |
| Linked list | Merge | Merging only relinks pointers, so no buffer is needed; quick sort depends on cheap random access. |
| k-th smallest value / median | Quick's partition (quickselect) | Recurse only on the side that holds k: n + n/2 + ... = O(n) on average. |

## Files

- [merge.py](merge.py): `merge_sort` and `test_*` functions with `assert`.
- [quick.py](quick.py): `quick_sort_lists`, `quick_sort` and `test_*` functions with `assert`; most tests run on both versions through the `SORTS` list.

Running each file executes all of its tests and prints `ok:` for each one that passes.

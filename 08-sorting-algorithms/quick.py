import random


def quick(nlist):
    nlist = list(nlist)
    size = len(nlist)
    
    if size <= 1:
        return nlist
    
    # Middle pivot: avoids the O(n²) worst case (and the recursion limit) on already sorted input.
    # Three-way partition keeps equal keys in their original order, so the sort is stable.
    pivot = nlist[size // 2]
    lr = [x for x in nlist if x < pivot]    # lower
    eq = [x for x in nlist if x == pivot]   # equal
    gt = [x for x in nlist if x > pivot]    # greater

    return quick(lr) + eq + quick(gt)


nums = [random.randint(0, 9) for _ in range(10)]
print(nums)
print(quick(nums))

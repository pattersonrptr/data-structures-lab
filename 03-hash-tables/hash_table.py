class HashTable:
    def __init__(self):
        self.table = [[] for _ in range(8)]
        self.count = 0
        self.load_factor_threshold = 0.75

    def _hash(self, key: object) -> int:
        return hash(key) % len(self.table)

    def _resize(self):
        old_table = self.table
        self.table = [[] for _ in range(len(old_table) * 2)]
        self.count = 0

        for bucket in old_table:
            for k, v in bucket:
                self.put(k, v)

    def put(self, key: object, value: object):
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.count += 1

        if self.count / len(self.table) > self.load_factor_threshold:
            self._resize()

    def get(self, key: object) -> object:
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                return v

        raise KeyError(f"Key '{key}' not found.")

    def remove(self, key: object):
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return

        raise KeyError(f"Key '{key}' not found.")

    def __len__(self):
        return self.count


NAMES = [
    "Patterson", "João", "Maria", "Ana", "Carlos", "Beatriz", "Pedro",
    "Juliana", "Lucas", "Fernanda", "Rafael", "Camila", "Gabriel",
]


def print_table(hash_table: HashTable):
    for index, bucket in enumerate(hash_table.table):
        print(f"  [{index:2}] {bucket}")


def demo_basic_operations():
    print("== Basic operations ==")
    hash_table = HashTable()
    assert len(hash_table) == 0

    hash_table.put("Patterson", 7)
    assert hash_table.get("Patterson") == 7
    assert len(hash_table) == 1

    # Same key again: the value is replaced and the count stays the same.
    hash_table.put("Patterson", 1)
    assert hash_table.get("Patterson") == 1
    assert len(hash_table) == 1

    hash_table.remove("Patterson")
    assert len(hash_table) == 0

    try:
        hash_table.get("Patterson")
        assert False, "get on a removed key should raise KeyError"
    except KeyError as ex:
        print(f"  get after remove -> KeyError: {ex}")

    try:
        hash_table.remove("Nobody")
        assert False, "remove on a missing key should raise KeyError"
    except KeyError as ex:
        print(f"  remove on missing key -> KeyError: {ex}")


def demo_collisions():
    print("== Collisions ==")
    hash_table = HashTable()

    # hash() on strings changes on every run, so a colliding pair can't be
    # hard-coded. With more names than buckets (13 > 8), at least two of them
    # are guaranteed to map to the same index.
    names_by_index = {}
    for name in NAMES:
        names_by_index.setdefault(hash_table._hash(name), []).append(name)
    first, second = next(g for g in names_by_index.values() if len(g) > 1)[:2]

    hash_table.put(first, 1)
    hash_table.put(second, 2)

    index = hash_table._hash(first)
    assert hash_table._hash(second) == index
    assert len(hash_table.table[index]) == 2  # both live in the same bucket
    assert hash_table.get(first) == 1  # ...and are still told apart
    assert hash_table.get(second) == 2
    assert len(hash_table) == 2
    assert len(hash_table.table) == 8  # no resize happened

    print(f"  '{first}' and '{second}' both hash to bucket {index}:")
    print_table(hash_table)


def demo_resize():
    print("== Resize ==")
    hash_table = HashTable()
    assert len(hash_table.table) == 8

    resized_at = []  # number of keys when each resize happened
    for position, name in enumerate(NAMES):
        size_before = len(hash_table.table)
        hash_table.put(name, position)
        size_after = len(hash_table.table)

        if size_after != size_before:
            resized_at.append(len(hash_table))
            print(f"  inserted '{name}' ({len(hash_table)} keys): "
                  f"{size_before} -> {size_after} buckets")

    # 7/8 = 0.875 > 0.75 and 13/16 = 0.8125 > 0.75 trigger the two resizes.
    assert resized_at == [7, 13]
    assert len(hash_table.table) == 32
    assert len(hash_table) == len(NAMES)

    # Every key must survive the rehash with its value intact.
    for position, name in enumerate(NAMES):
        assert hash_table.get(name) == position

    print_table(hash_table)


if __name__ == "__main__":
    demo_basic_operations()
    demo_collisions()
    demo_resize()
    print("All checks passed.")

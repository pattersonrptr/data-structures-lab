class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.count = 0

    def get(self, index: int):
        if index < 0 or index >= self.count:
            raise ValueError(f'Invalid position: {index}.')

        temp = self.first

        for _ in range(index):
            temp = temp.next
            
        return temp
    
    def _insert (self, value, index: int):
        if index < 0 or index > self.count:
            raise ValueError(f'Invalid position: {index}.')

        new_node = Node(value)

        if not self.first:
            self.first = new_node
            self.last = new_node
        elif self.count == index:
            self.last.next = new_node
            self.last = new_node
        elif index == 0:
            new_node.next = self.first
            self.first = new_node
        else:
            temp = self.get(index - 1)
            new_node.next = temp.next
            temp.next = new_node

        self.count += 1

    def append(self, value):
        self._insert(value, len(self))

    def insert(self, value, index):
        self._insert(value, index)

    def prepend(self, value):
        self._insert(value, 0)

    def contains(self, value):
        current = self.first

        while current:
            if current.value == value:
                return True
            current = current.next

        return False

    def remove(self, value):
        current = self.first
        previous = None
        
        while current:
            if current.value == value:
                if previous:
                    previous.next = current.next
                else:
                    self.first = current.next

                if self.last is current:
                    self.last = previous

                current.next = None
                self.count -= 1
                return 
                
            previous = current
            current = current.next

        raise ValueError("Value not found")
        

    def to_list(self):
        return [v for v in self]

    def __iter__(self):
        current = self.first

        while current:
            yield current.value
            current = current.next

    def __len__(self):
        return self.count



if __name__ == "__main__":
    linked_list = LinkedList()
    
    for i in range(10):
        linked_list.prepend(f'Value {i}')

    for i in range(len(linked_list)):
        print(linked_list.get(i).value)

    print("-" * 20)

    linked_list.insert('Teste', 2)

    for i in range(len(linked_list)):
        print(linked_list.get(i).value)

    linked_list.append('Teste 2')

    print("-" * 20)

    for i in range(len(linked_list)):
        print(linked_list.get(i).value)

    print("-" * 20)

    print(linked_list.contains("Value 9"))

    print("List size: ", len(linked_list))
    linked_list.remove("Value 9")
    linked_list.remove("Teste")
    linked_list.remove("Teste 2")
    for i in range(len(linked_list)):
        print(linked_list.get(i).value)
    try:
        linked_list.remove("Value 9")
        linked_list.remove("Teste")
        linked_list.remove("Teste 2")
    except ValueError as ex:
        print(ex)

    print(linked_list.contains("Value 9"))
    print("List size: ", len(linked_list))

    print("-" * 20)

    for i in range(len(linked_list)):
        print(linked_list.get(i).value)

    print("-" * 20)

    for value in linked_list:
        print(value)

    print("-" * 20)

    print(linked_list.to_list())

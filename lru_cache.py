class lru_cache:
    def __init__(self, capacity):
        """LRU cache constructor."""
        self.capacity = capacity
        self.node_map = {}
        self.sentinel = Node(None, None, True)
        self.head = self.sentinel
        self.tail = self.sentinel

    def __push(self, key, value):
        """Push entry to the front of the queue."""
        # Create node storing key and value.
        node = Node(key, value)

        # Push node onto queue.
        node.next = self.head
        if self.tail.is_sentinel:
            self.tail = node
            self.tail.next = self.sentinel
        else:
            self.head.prev = node
        self.head = node

        # Map key to node to allow in-place deletion later.
        self.node_map[key] = node

    def __pop(self):
        """Pop entry from the back of the queue."""
        # Make copy of tail node contents.
        key = self.tail.key
        value = self.tail.value

        # Delete tail node in-place.
        self.tail.next = None
        self.tail.is_sentinel = True
        self.sentinel.prev = None
        self.sentinel = self.tail

        # Set new tail if necessary.
        new_tail = self.tail.prev
        if new_tail is not None:
            new_tail.next = self.tail
            self.tail.prev = new_tail
            self.tail = new_tail

        return Node(key, value)

    def __getitem__(self, key):
        """Get value associated with key if the key exists in the cache."""
        if key in self.node_map.keys():
            node = self.node_map[key]
            if node == self.head:
                return node.value 
            # Delete node in-place.
            node.prev.next = node.next
            node.next.prev = node.prev
            # Push node to the front of the queue.
            self.__push(node.key, node.value)
            return node.value
        else:
            raise KeyError("Cache miss!")

    def __setitem__(self, key, value):
        """Map key to value in cache."""
        if key in self.node_map.keys():
            # Retrieving old value moves it to the front of the queue as a
            # side-effect (ugly but avoids code duplication).
            old_value = self[key]
            # Then we simply need to set its value to value.
            self.head.value = value
        else:
            self.__push(key, value)
            # If we have exceeded capacity, then we need to evict the entry.
            if len(self.node_map.keys()) > self.capacity:
                # Evict the least recently used.
                evicted = self.__pop()
                # remove the entry from our node map.
                del self.node_map[evicted.key]


class Node(object):
    """Doubly linked list node class for LRU Cache."""
    def __init__(self, key, value, is_sentinel=False):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None       
        self.is_sentinel = is_sentinel

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

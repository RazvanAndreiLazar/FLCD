class ListNode:
    def __init__(self, value, next = None) -> None:
        self.__value = value
        self.__next = next

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def set_next(self, next):
        self.__next = next

    def get_next(self):
        return self.__next

class LinkedList:
    def __init__(self) -> None:
        self.__head :ListNode = None
        self.__tail :ListNode = None

    def get_head(self):
        return self.__head

    def get_tail(self):
        return self.__tail

    def insert(self, value):
        node = ListNode(value)
        if self.__head is None:
            self.__head = node
            self.__tail = node
            return

        self.__tail.set_next(node)
        self.__tail = node

    def __str__(self):
        current = self.__head
        s = ''
        while current is not None:
            key, val = current.get_value()
            s += str(key) + ': ' + str(val) + '\n'

            current = current.get_next()

        return s

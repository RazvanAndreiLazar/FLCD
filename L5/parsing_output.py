from grammar import Production
from collections import deque

class Node:
    def __init__(self, child, right_sibling, value, depth) -> None:
        self.__child: Node = child
        self.__right_sibling: Node = right_sibling
        self.__value = value
        self.__depth = depth

    @property
    def child(self):
        return self.__child
    @child.setter
    def child(self, val):
        self.__child = val

    @property
    def right_sibling(self):
        return self.__right_sibling
    @right_sibling.setter
    def right_sibling(self, val):
        self.__right_sibling = val

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self, val):
        self.value = val

    @property
    def depth(self):
        return self.__depth
    @depth.setter
    def depth(self, val):
        self.depth = val

    def __str__(self) -> str:
        return f"{self.__value}({self.depth})" 

class ParsingOutput:
    def __init__(self) -> None:
        self.__head = None

    def search_bfs(self, value, without_child = True):
        dq = deque()
        dq.append(self.__head)        

        while len(dq):
            current_node: Node = dq.popleft()

            if current_node.value == value:
                if (without_child):
                    if current_node.child == None:
                        return current_node
                else:
                    return current_node

            if (current_node.right_sibling != None): dq.appendleft(current_node.right_sibling)
            if (current_node.child != None): dq.append(current_node.child)


        return None

    def add_bfs(self, parent_val, children_values):
        parent = self.search_bfs(parent_val) if self.__head is not None else Node(None, None, parent_val, 0)
        self.__head = parent if self.__head is None else self.__head

        right_sibling = None
        for i in range(len(children_values) - 1, -1, -1):
            right_sibling = Node(None, right_sibling, children_values[i], parent.depth + 1)
        parent.child = right_sibling
        right_sibling

    def add_production(self, production: Production, current_leftmost_sibling: Node):
        parent = production.lhs
        children = production.rhs.split()

        print(f"Parent: {parent}, children: {children}")

        self.add_bfs(parent, children)

    def process_parser_output(self, production_list):
        current_leftmost_sibling = None

        for production in production_list:
            self.add_production(production, current_leftmost_sibling)

    def bf_parse(self):
        bf = []
        dq = deque()
        dq.append(self.__head)        

        while len(dq):
            current_node: Node = dq.popleft()
            bf.append(current_node)

            if (current_node.right_sibling != None): dq.appendleft(current_node.right_sibling)
            if (current_node.child != None): dq.append(current_node.child)

        return bf

    def __str__(self) -> str:
        s = ''
        s += self.__head
        return s
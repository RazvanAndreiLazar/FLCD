from HashTable import HashTable

class SymbolTable(HashTable):
    __index = 0
    def __init__(self) -> None:
        super().__init__()

    def insert(self, key):
        SymbolTable.__index += 1
        return super().insert(key, SymbolTable.__index)

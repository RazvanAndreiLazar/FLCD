class PifField:
    def __init__(self, key, token_index, table_index) -> None:
        self.key = key
        self.token_index = token_index
        self.table_index = table_index

class PifReader:
    def __init__(self) -> None:
        self.__pif = []

    def readPIF(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                key, val = line.split(':')
                val.strip('()')
                token_index, table_index = val.split(',')

                self.__pif.append(PifField(key, token_index, table_index))

    def get_keys(self):
        return [x.key for x in self.__pif]
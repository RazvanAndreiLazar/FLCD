from SymbolTable import SymbolTable
import re

class Scanner:
    def __init__(self, file, tokens_file = "L2/tokens.in"):
        self.__file = file
        self.__tokens_file = tokens_file
        self.__tokens = {}

    def set_file(self, file):
        self.__file = file

    def read_tokens(self):
        f = open(self.__tokens_file, "r")
        for i, line in enumerate(f.readlines()):
            self.__tokens[line.strip()] = i


    def scan(self) -> tuple():
        identifier_st = SymbolTable()
        constant_st = SymbolTable()

        f = open(self.__file, "r")

        for line in f.readlines():
            self._parse_line(line, identifier_st, constant_st)

        f.close()
        
        print()
        print('IDENTIFIERS', identifier_st, sep='\n')
        print('CONSTANTS', constant_st, sep='\n')

    def _parse_line(self, line: str, identifier_st: SymbolTable, constant_st: SymbolTable):
        words = line.split()

        for word in words:
            if self.__process_word(word, identifier_st, constant_st):
                continue

            token = ''
            for i in range(0, len(word)):
                c = word[i]

                if c == '_' or \
                (c >= 'a' and c <= 'z') or \
                (c >= 'A' and c <= 'Z') or \
                (c >= '0' and c <= '9'):
                    token += c
                    continue

                if i < len(word) - 1 and c + word[i+1] in self.__tokens:
                    self.__process_word(token, identifier_st, constant_st)
                    token = ''
                    continue

                if c in self.__tokens:
                    self.__process_word(token, identifier_st, constant_st)
                    token = ''
                    continue

            if token != '': self.__process_word(token, identifier_st, constant_st)

    def __process_word(self, word, identifier_st, constant_st):
        print(word)

        if word in self.__tokens.keys():
            #TODO: put it into PIF
            return True

        if self.__is_identifier(word):
            if identifier_st.search(word) is None:
                identifier_st.insert(word)
            return True

        if self.__is_constant(word):
            if constant_st.search(word) is None:
                constant_st.insert(word)
            return True
        return False

    def __is_identifier(self, word):
        regex = '_?[a-zA-Z]([a-zA-Z0-9])*'
        return re.fullmatch(regex, word) != None

    def __is_constant(self, word):
        intregex = '[+-]?[0-9]+'
        charregex = "'.'"
        strregex = '".*"'
        return (re.fullmatch(intregex, word) != None) | \
            (re.fullmatch(charregex, word) != None) | \
            (re.fullmatch(strregex, word) != None) | \
            (word == "true") | (word == "false")


line = 'if (a == 2)'

ist = SymbolTable()
cst = SymbolTable()

scn = Scanner('L1/p1.txt')
scn.read_tokens()
scn.scan()
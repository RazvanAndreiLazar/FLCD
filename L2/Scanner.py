from SymbolTable import SymbolTable
import re

class Scanner:
    def __init__(self, file, tokens_file = "L1b/tokens.in"):
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

        return identifier_st, constant_st

    def _parse_line(self, line: str, identifier_st: SymbolTable, constant_st: SymbolTable):
        # split the line into words by space 
        words = line.split()

        for word in words:
            # check if the word can be classified as an token, identifier or constant
            if self.__process_word(word, identifier_st, constant_st):
                continue
            
            # if the entire word is not a token try to sepparate it into tokens character by character
            token = ''
            for i in range(0, len(word)):
                c = word[i]

                # if the character is part of the alphabet, but not a separator or operand add it to the token and go to the next one
                if c == '_' or \
                (c >= 'a' and c <= 'z') or \
                (c >= 'A' and c <= 'Z') or \
                (c >= '0' and c <= '9'):
                    token += c
                    continue

                # if the current character and the next one form an operator process the previous token and reset it
                if i < len(word) - 1 and c + word[i+1] in self.__tokens:
                    self.__process_word(token, identifier_st, constant_st)
                    token = ''
                    continue
                # if the current character is an operator or separator process the previous token and reset it
                if c in self.__tokens:
                    self.__process_word(token, identifier_st, constant_st)
                    token = ''
                    continue

            # process the last token in the line
            if token != '': self.__process_word(token, identifier_st, constant_st)

    def __process_word(self, word, identifier_st, constant_st):
        # print(word)
        # if the word is a token put it into pif
        if word in self.__tokens.keys():
            #TODO: put it into PIF
            return True
        # if the word is an identifier add it to the identifiers symbol table
        if self.__is_identifier(word):
            if identifier_st.search(word) is None:
                identifier_st.insert(word)
            return True
        # if the word is a constant add it to the constants symbol table
        if self.__is_constant(word):
            if constant_st.search(word) is None:
                constant_st.insert(word)
            return True

        return False

    def __is_identifier(self, word):
        regex = '_?[a-zA-Z]([a-zA-Z0-9])*'      # regex for identifiers in the programming language
        return re.fullmatch(regex, word) != None

    def __is_constant(self, word):
        intregex = '[+-]?[0-9]+'         # regex for int constants in the programming language
        charregex = "'.'"                # regex for char constants in the programming language
        strregex = '".*"'                # regex for string constants in the programming language
        return (re.fullmatch(intregex, word) != None) | \
            (re.fullmatch(charregex, word) != None) | \
            (re.fullmatch(strregex, word) != None) | \
            (word == "true") | (word == "false")



ist = SymbolTable()
cst = SymbolTable()

scn = Scanner('L1a/p1.txt')
scn.read_tokens()
identifier_st, constant_st = scn.scan()
        
print()
print('IDENTIFIERS', identifier_st, sep='\n')
print('CONSTANTS', constant_st, sep='\n')
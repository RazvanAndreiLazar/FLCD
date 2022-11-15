from enum import Enum
import string
from L4.FiniteAutomata import FiniteAutomata
from LinkedList import LinkedList
from SymbolTable import SymbolTable
import re

class TokenType (Enum):
    IDENT = 0
    CONST = 1
    TOKEN = 2
class Scanner:

    def __init__(self, file, tokens_file = "../L1b/tokens.in"):
        self.__file = file
        self.__tokens_file = tokens_file
        self.__tokens = {}

        self.__pif = LinkedList()
        self.__identifier_st = SymbolTable()
        self.__constant_st = SymbolTable()

        self.__identifier_fa = FiniteAutomata()
        self.__identifier_fa.readFA('../L4/IdentifiersFA.in')
        self.__int_const_fa = FiniteAutomata()
        self.__int_const_fa.readFA('../L4/IntConstFA.in')

    def set_file(self, file):
        self.__file = file

    def read_tokens(self):
        self.__tokens['const'] = 0
        self.__tokens['ident'] = 1

        f = open(self.__tokens_file, "r")
        for i, line in enumerate(f.readlines()):
            self.__tokens[line.strip()] = i + 2


    def scan(self) -> tuple():
        self.__identifier_st = SymbolTable()
        self.__constant_st = SymbolTable()
        self.__pif = LinkedList()

        f = open(self.__file, "r")

        for line_no, line in enumerate(f.readlines()):
            res = self._parse_line(line)
            if res is not None:
                return (False, (line_no, res))

        f.close()

        return (True, (self.__pif, self.__identifier_st, self.__constant_st))

    def _parse_line(self, line: str):
        # separate string constants from the rest of the parse
        res, string_sepp = self.__separate_from_strings(line)

        if not res: return string_sepp

        for i, elem in enumerate(string_sepp):
            if (i % 2 == 0):
                res = self.__parse_elem(elem) 
                if res is not None:
                    return res
            else: 
                self.__process_word('"' + elem + '"')
        
        return None


    def __parse_elem(self, elem):
        # split the line into words by space 
        words = elem.split()

        for word in words:
            # check if the word can be classified as an token, identifier or constant
            if self.__process_word(word):
                continue
            
            # if the entire word is not a token try to separate it into tokens character by character
            token = ''
            i = 0
            while i < len(word):
                c = word[i]

                # if the character is part of the alphabet, but not a separator or operand add it to the token and go to the next one
                if c == '_' or \
                (c >= 'a' and c <= 'z') or \
                (c >= 'A' and c <= 'Z') or \
                (c >= '0' and c <= '9'):
                    token += c
                    i += 1
                    continue

                # if the current character and the next one form an operator process the previous token and reset it
                if i < len(word) - 1 and c + word[i+1] in self.__tokens:
                    if token != '' and not self.__process_word(token):
                        return token
                    self.__add_to_pif(c + word[i+1], TokenType.TOKEN)
                    token = ''
                    i += 2
                    continue
                # if the current character is an operator or separator process the previous token and reset it
                if c in self.__tokens:
                    if token != '' and not self.__process_word(token):
                        return token
                    self.__add_to_pif(c, TokenType.TOKEN)
                    token = ''
                    i += 1
                    continue
                
                print(c)
                return c

            # process the last token in the line
            if token != '' and not self.__process_word(token):
                return token

        return None

    def __process_word(self, word):
        # if the word is a token put it into pif
        if word in self.__tokens.keys():
            self.__add_to_pif(word, TokenType.TOKEN)
            return True
        # if the word is an identifier add it to the identifiers symbol table
        if self.__is_identifier(word):
            if self.__identifier_st.search(word) is None:
                self.__identifier_st.insert(word)
            
            self.__add_to_pif(word, TokenType.IDENT)
            return True
        # if the word is a constant add it to the constants symbol table
        if self.__is_constant(word):
            if self.__constant_st.search(word) is None:
                self.__constant_st.insert(word)
            
            self.__add_to_pif(word, TokenType.CONST)
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

    def __add_to_pif(self, word, type: TokenType):
        if type == TokenType.IDENT:
            self.__pif.insert((word, (0, self.__identifier_st.search(word))))
        if type == TokenType.CONST:
            self.__pif.insert((word, (1, self.__constant_st.search(word))))
        if type == TokenType.TOKEN:
            self.__pif.insert((word, (self.__tokens[word], -1)))

    def __separate_from_strings(self, line: str):
        tokens = line.split('"')

        if (len(tokens) % 2 == 0):
            return False, tokens[-1]
        
        return True, tokens



class FiniteAutomata():
    @property
    def alphabet(self):
        return self.__alphabet

    @property
    def states(self):
        return self.__states

    @property
    def final_states(self):
        return self.__final_states

    @property
    def initial_state(self):
        return self.__initial_state

    @property
    def transitions(self):
        return self.__transitions


    def __init__(self):
        self.__alphabet = set()
        self.__states = set()
        self.__final_states = set()
        self.__initial_state = None
        self.__transitions = {}


    def readFA(self, filename: str):
        file = open(filename, 'r')
        
        for line in file.readlines():
            line = line.strip()
            id, val = line.split(':')
            if id == 'STATES': self.__read_states(val) 
            elif id == 'ALPHABET': self.__read_alphabet(val)
            elif id == 'INITIAL_STATE': self.__read_initial_state(val)
            elif id == 'FINAL_STATES': self.__read_final_states(val)
            elif id == 'TRANSITIONS': self.__read_transitions(val)

    def __read_states(self, states: str):
        for token in states.split('|'):
            self.__states.add(token)

    def __read_alphabet(self, alphabet: str):
        for token in alphabet.split('|'):
            self.__alphabet.add(token)

    def __read_initial_state(self, init_state: str):
        self.__initial_state = init_state

    def __read_final_states(self, states: str):
        for token in states.split('|'):
            self.__final_states.add(token)

    def __read_transitions(self, transactions: str):
        for token in transactions.split('|'):
            key, value = token.split(' -> ')
            state, transaction = key.split(' + ')

            self.__transitions[(state, transaction)] = value


    def verify(self, token: str):
        state = self.__initial_state

        for l in token:
            if l not in self.__alphabet:
                return False
            if (state, l) not in self.__transitions:
                return False

            state = self.__transitions[(state, l)]

        return state in self.__final_states
            

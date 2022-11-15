from FiniteAutomata import FiniteAutomata

fa = FiniteAutomata()

fa.readFA('L4/IntConstFA.in')

def print_menu():
    print("0. EXIT")
    print("1. Alphabet")
    print("2. States")
    print("3. Final states")
    print("4. Initial state")
    print("5. Transitions")
    print("6. Verify token")

while(True):
    print_menu()
    choice = input()
    if choice == '0':
        break
    elif choice == '1':
        print(fa.alphabet)
    elif choice == '2':
        print(fa.states)
    elif choice == '3':
        print(fa.final_states)
    elif choice == '4':
        print(fa.initial_state)
    elif choice == '5':
        print(fa.transitions)
    elif choice == '6':
        print('Token:', end=' ')
        token = input()
        print(fa.verify(token))

    print()
        
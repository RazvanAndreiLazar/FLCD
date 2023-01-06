
from Scanner import Scanner

def logPIF(pif):
    try:
        f = open('L3/PIF.out', 'w')
    except FileNotFoundError:
        f = open('../L3/PIF.out', 'w')
    finally:
        f.write(str(pif))
        f.close()


def logST(id_st, cst_st):
    try:
        f = open('L3/ST.out', 'w')
    except FileNotFoundError:
        f = open('../L3/ST.out', 'w')
    finally:
        f.write('Symbol table representation: 2 Hash Tables, one for constant ST, one for identifier ST\n')
        f.write('IDENTIFIERS:\n' + str(id_st) + '\n')
        f.write('CONSTANTS:\n' + str(cst_st) + '\n')



print("Filename: ", end='')
filename = input()

scn = Scanner('../L1a/p3.txt' if filename.strip() == '' else filename)
scn.read_tokens()
flag, res = scn.scan()

if flag:
    pif, identifier_st, constant_st = res
        
    print()
    print('lexically correct')
    logPIF(pif)
    logST(identifier_st, constant_st)

else:
    line_no, token = res
    print('lexical error: ' + str(token) + ' (on line: ' + str(line_no) + ')')
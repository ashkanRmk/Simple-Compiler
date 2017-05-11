from AutomataTheory import *

def main():
    inp = raw_input("Please Enter your REGEX: ")
    print "Regular Expression: ", inp
    nfaObj = NFAfromRegex(inp)
    nfa = nfaObj.getNFA()
    dfaObj = DFAfromNFA(nfa)
    # dfa = dfaObj.getDFA()
    # minDFA = dfaObj.getMinimisedDFA()
    print "\nNFA: "
    nfaObj.displayNFA()
    print "\nDFA: "
    dfaObj.displayDFA()
    print "\nMinimised DFA: "
    dfaObj.displayMinimisedDFA()


if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        print("\nFailure:", e)

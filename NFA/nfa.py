"""
    Input file format:
       [STATES] - on every line: state_name [, start] / [, end] (one state need to be labeled as start, another as end)
       [SIGMA] - input alphabet (one symbol for every line)
       [RULES] - transition rules: source_state, symbol, destination_state
       [END] - marks the end of a section
       Comments : #
"""
import sys

EPS = "ε"
def load_nfa(fn: str):
    nfa = dict()
    # read from file and ignore comments and empty lines
    with open(fn) as f:
        lines = [line.split("#", 1)[0].strip() for line in f if line.split("#", 1)[0].strip()]

    # extract sections

    i = 0
    while i < len(lines):
        if lines[i][0] == '[':
            sec = lines[i][1:-1].lower()
            i += 1
            while lines[i].upper() != '[END]':
                if sec not in nfa:
                    nfa[sec] = []
                nfa[sec].append(lines[i])
                i += 1
        i += 1

    # check if [STATES], [SIGMA], [RULES] sections are present

    for req in ('states', 'sigma', 'rules'):
        if req not in nfa:
            f"Missing [{req.upper()}] section!"

    # process data from [STATES]
    state_rows = nfa['states']
    names, finals = [], []
    start = None

    for row in state_rows:
        parts = [p.strip() for p in row.split(',')]
        q = parts[0]
        names.append(q)

        if len(parts) > 1 and parts[1] == 'start':
            start = q
        if len(parts) > 1 and parts[1] == 'end':
            finals.append(q)

    nfa['states'] = names
    nfa['start']  = start
    nfa['finals'] = finals

    if 'sigma' not in nfa:
        nfa['sigma'] = []

    rule_rows = nfa['rules']
    nfa['rules'] = []

    for rule_line in rule_rows:
        src_state, input_symbol, dest_state = [field.strip() for field in rule_line.split(',')]

        if input_symbol.lower() in ('eps', 'epsilon'):
            input_symbol = EPS

        nfa['rules'].append((src_state, input_symbol, dest_state))

    return nfa

def epsilon_closure(states, rules):
    # all states accessible only through ε from every state from 'states'.
    stack = list(states)
    closure = set(states)
    while stack:
        q = stack.pop()
        for p, a, r in rules:
            if p == q and a == EPS and r not in closure:
                closure.add(r)
                stack.append(r)
    return list(closure)

def is_nfa_valid(test, nfa):

    current = epsilon_closure({nfa['start']}, nfa['rules'])

    # go through all symbols
    for sym in test:
        next_states = []

        for q in current:
            for p, a, r in nfa['rules']:
                if p == q and a == sym:
                    next_states.append(r)

        #  close ε  over the newly reached states
        current = epsilon_closure(next_states, nfa['rules'])

        # If there is no more acceptable branch -> REJECT
        if not current:
            return False

    # ACCEPT if every current state is final
    return any(q in nfa['finals'] for q in current)

def main():
    n = len(sys.argv)  # number of arguments                                                       

    # run command line arguments (if they exist)                                                  
    if n > 1:
        try:
            # first argument = NFA file                                                           
            with open(sys.argv[1]) as file:
                print(f"-> Read NFA from {file.name}")
                nfa = load_nfa(file.name)
        except FileNotFoundError:
            print(f"Error: file '{sys.argv[1]}' not found.")
            sys.exit(1)

        print('--- COMMAND LINE ARGUMENTS ---')
        for i in range(2, n):
            if is_nfa_valid(sys.argv[i], nfa) == True:
                print(f"String {sys.argv[i]}: PASSED")
            else:
                print(f"String {sys.argv[i]}: REJECTED")

    else:
        # default tests if not
        print("accept_ending_with_01_NFA.txt:")
        nfa = load_nfa("accept_ending_with_01_NFA.txt")
        tests = ["", "0", "01", "001", "0011", "00110", "11001"]
        for test in tests:
            if is_nfa_valid(test, nfa) == True:
                print(f"String {test}: PASSED")
            else:
                print(f"String {test}: REJECTED")

        print()

        print("accept_1_on_3rd_pos_from_end_NFA.txt:")
        nfa = load_nfa("accept_1_on_3rd_pos_from_end_NFA.txt")
        tests = ["", "0", "01", "001", "0011", "00110", "11001", "1100", "00110011001100"]
        for test in tests:
            if is_nfa_valid(test, nfa) == True:
                print(f"String {test}: PASSED")
            else:
                print(f"String {test}: REJECTED")

        print()
        print("DFA_accept_1_on_3rd_pos_from_end_NFA.txt:")
        nfa = load_nfa("DFA_accept_1_on_3rd_pos_from_end_NFA.txt")
        tests = ["", "0", "01", "001", "0011", "00110", "11001", "1100", "00110011001100"]
        for test in tests:
            if is_nfa_valid(test, nfa) == True:
                print(f"String {test}: PASSED")
            else:
                print(f"String {test}: REJECTED")


if __name__ == "__main__":
    main()
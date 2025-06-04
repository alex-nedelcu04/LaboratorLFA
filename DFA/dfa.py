"""
    Input file format:
       [STATES] - on every line: state_name [, start] / [, end] (one state need to be labeled as start, another as end)
       [SIGMA] - input alphabet (one symbol for every line)
       [RULES] - transition rules: source_state, symbol, destination_state
       [END] - marks the end of a section
       Comments : #
"""
import sys

def load_dfa(fn: str):
    dfa = dict()
    with open(fn) as f:
        # read from file and ignore comments and empty lines
        lines = [line.split("#", 1)[0].strip() for line in f if line.split("#", 1)[0].strip()]
        idx_line = 0
        num_lines = len(lines)
        while idx_line < num_lines:
            # go through lines until finding [STATES], [SIGMA] or [RULES]
            while lines[idx_line][0] != '[' and lines[idx_line][-1] != ']':
                idx_line += 1
            if lines[idx_line].upper() != '[END]':
                argument = lines[idx_line][1:-1].lower()
                idx_line += 1
                # go through the section's arguments until finding [END]
                while lines[idx_line].upper() != '[END]':
                    if argument not in dfa.keys():
                        dfa[argument] = [lines[idx_line]]
                    else:
                        dfa[argument].append(lines[idx_line])

                    idx_line += 1

            idx_line += 1

    # check if all sections are present
    for req in ('states', 'sigma', 'rules'):
        if req not in dfa:
            print(f"Missing [{req.upper()}] section!")
            
    # data processing from [STATES] to obtain start and end states

    found_start = False
    found_end = False
    for idx_state in range(len(dfa['states'])):
        dfa['states'][idx_state] = [elem.strip() for elem in  dfa['states'][idx_state].split(',')]
        if len(dfa['states'][idx_state]) == 2 and dfa['states'][idx_state][1] == 'start':
            dfa['start'] =  dfa['states'][idx_state][0]
            found_start = True
        elif len(dfa['states'][idx_state]) == 2 and  dfa['states'][idx_state][1] == 'end':
            dfa['F'] =  dfa['states'][idx_state][0]
            found_end = True
        dfa['states'][idx_state] = dfa['states'][idx_state][0]

    if found_start == False and found_end == False:
        print("No start state and no end state found!")
        return

    if found_start == False:
        print ("No start state found!")
        return

    if found_end == False:
        print("No end state found!")
        return

    # data processing from [RULES] to be able to later verify the validity of every rule
    # ex.: 'q0, 0, q1'; => [q0, 0 , q1]

    for idx_rule in range(len(dfa["rules"])):
        dfa['rules'][idx_rule] = list(dfa['rules'][idx_rule].split(','))
        dfa['rules'][idx_rule] = [elem.strip() for elem in dfa['rules'][idx_rule]]

    # verify rule validity

    for idx_rule in range(len(dfa["rules"])):
        if len(dfa["rules"][idx_rule]) != 3:
            print("Too many arguments in rule!")
            return
        start_state = dfa["rules"][idx_rule][0]
        sigma_value = dfa["rules"][idx_rule][1]
        end_state = dfa["rules"][idx_rule][2]
        if start_state not in dfa["states"]:
            print(f"State {start_state} does not exist!")
            return

        if end_state not in dfa["states"]:
            print(f"State {end_state} does not exist!")
            return
        if sigma_value not in dfa["sigma"]:
            print(f"Sigma value {sigma_value} does not exist!")
            return

    return dfa

def is_dfa_valid(word: str, dfa: dict) -> bool:

    current_state = dfa['start']
    for symbol in word:
        if symbol not in dfa['sigma']:
            print(f"Symbol '{symbol}' doesn't exist in this DFA's alphabet!")
            return False
        # search for corresponding transition
        next_state = None
        for rule in dfa['rules']:
            if rule[0] == current_state and rule[1] == symbol:
                next_state = rule[2]
                break
        if next_state is None:
            return False
        current_state = next_state
    return current_state == dfa['F']

def main():


    n = len(sys.argv) # number of arguments

    # run command line arguments (if they exist)
    if n > 1:
        try:
            # first argument = DFA file
            with open(sys.argv[1]) as file:
                print(f"-> Read DFA from {file.name}")
                dfa = load_dfa(file.name)
        except FileNotFoundError:
            print(f"Error: file '{sys.argv[1]}' not found.")
            sys.exit(1)

        print('--- COMMAND LINE ARGUMENTS ---')
        for i in range(2, n):
            if is_dfa_valid(sys.argv[i], dfa) == True:
                print(f"String {sys.argv[i]}: PASSED")
            else:
                print(f"String {sys.argv[i]}: REJECTED")

    else:
        # default tests if not
        print(f"-> Read DFA from automata_DFA.txt")
        dfa = load_dfa("automata_DFA.txt")

        tests = ["", "0", "00", "1", "01", "001", "010", "0101", "0100", "0001110", "0001011"]
        for test in tests:
            if is_dfa_valid(test, dfa) == True:
                print(f"String {test}: PASSED")
            else:
                print(f"String {test}: REJECTED")


if __name__ == "__main__":
    main()
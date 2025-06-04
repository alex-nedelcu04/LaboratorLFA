"""
    Input file format:
       [STATES] - on every line: state_name [, start] / [, end] (one state need to be labeled as start, another as end)
       [SIGMA] - input alphabet (one symbol for every line)
       [GAMMA] - stack symbol
       [RULES] - transition rules: source_state, symbol_input (or eps), stack_pop (or eps), destination_state, stack_push (or eps)
       [END] - marks the end of a section
       Comments : #
"""

import sys

EPS = "ε"
DOLLAR = "$"

def load_pda(filename: str):
    # read from file and ignore comments and empty lines  
    sections =  dict()
    with open(filename) as f:
        lines = [line.split("#", 1)[0].strip() for line in f if line.split("#", 1)[0].strip()]

    i = 0
    while i < len(lines):
        if lines[i][0] == '[':
            sec_name = lines[i][1:-1].lower()
            i += 1
            if sec_name not in sections:
                sections[sec_name] = []
            while lines[i].upper() != '[END]':
                sections[sec_name].append(lines[i])
                i += 1
        i += 1


    # STATES
    
    states = []
    finals = []
    start = None

    state_rows = sections['states'] if 'states' in sections else []
    for row in state_rows:
        parts = [p.strip() for p in row.split(',')]
        q = parts[0]
        states.append(q)
        if len(parts) > 1:
            tag = parts[1].lower()
            if tag == 'start':
                start = q
            if tag == 'end':
                finals.append(q)

    pda = dict()
    pda['states'] = states
    pda['start'] = start
    pda['finals'] = finals
    pda['sigma'] = sections['sigma'] if 'sigma' in sections else []
    pda['gamma'] = sections['gamma'] if 'gamma' in sections else []
    pda['rules'] = []

    # TRANSITIONS
    
    if 'rules' in sections:
        for r in sections['rules']:
            q, a, X, p, push = (x.strip() for x in r.split(','))
            if a.lower() in ('eps', 'epsilon'):
                a = EPS
            if X.lower() in ('eps', 'epsilon'):
                X = EPS
            if push.lower() in ('eps', 'epsilon'):
                push = EPS
            pda['rules'].append((q, a, X, p, push))

    # check if [STATES], [SIGMA], [RULES] sections are present    

    for req in ('states', 'sigma', 'gamma', 'rules'):
        if req not in pda:
            f"Missing [{req.upper()}] section!"

    return pda

def is_pda_valid(word: str, pda, max_steps: int = 10000) -> bool:
    queue = [[pda['start'], 0, DOLLAR]]
    visited = [queue[0]]
    steps = 0

    while queue and steps < max_steps:
        # remove first element
        state, pos, stack = queue.pop(0)
        steps += 1

        # accept if the whole string was read and the state is a final one
        if pos == len(word) and state in pda['finals']:
            return True

        top = stack[-1] if stack else EPS

        # fo through every rule that begin from the current state
        for rule in pda['rules']:
            q_src, symbol_input, stack_pop, q_dest, push = rule
            if q_src != state:
                continue

            # matching on starting symbol
            if symbol_input != EPS:
                if pos >= len(word) or word[pos] != symbol_input:
                    continue
                new_pos = pos + 1
            else:
                new_pos = pos

            # matching on the top of the stack
            if stack_pop != EPS and top != stack_pop:
                continue

            # build new stack
            new_stack = stack
            if stack_pop != EPS:  # POP
                new_stack = new_stack[:-1]
            if push != EPS:  # PUSH 
                new_stack = new_stack + push[::-1]

            new_config = [q_dest, new_pos, new_stack or ""]
            if new_config not in visited:
                visited.append(new_config)
                queue.append(new_config)

    return False

def main():
    n = len(sys.argv)  # number of arguments                                                           

    # run command line arguments (if they exist)                                                      
    if n > 1:
        try:
            # first argument = PDA file                                                               
            with open(sys.argv[1]) as file:
                print(f"-> Read PDA from {file.name}")
                pda = load_pda(file.name)
        except FileNotFoundError:
            print(f"Error: file '{sys.argv[1]}' not found.")
            sys.exit(1)

        print('--- COMMAND LINE ARGUMENTS ---')

        for i in range(2, n):
            if is_pda_valid(sys.argv[i], pda) == True:
                print(f"String {sys.argv[i]}: PASSED")
            else:
                print(f"String {sys.argv[i]}: REJECTED")

    else:
        # default tests if not
        print(f"-> Read PDA from a^n-b^n_PDA.txt")
        pda = load_pda("a^n-b^n_PDA.txt")

        tests = ["", "ab", "aabb", "aaabbb", "aab", "abb"]
        for test in tests:
            if is_pda_valid(test, pda) == True:
                print(f"String {test}: PASSED")
            else:
                print(f"String {test}: REJECTED")

        print()

        print(f"-> Read PDA from parentheses_PDA.txt")
        pda = load_pda("parentheses_PDA.txt")

        tests = ["", "()", "(())", "()()", "(()())", "(()", "())(", ")(()"]
        for test in tests:
            if is_pda_valid(test, pda) == True:
                print(f"String {test}: PASSED")
            else:
                print(f"String {test}: REJECTED")

        print()

if __name__ == "__main__":
    main()
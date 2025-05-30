"""
Format fişier symbol_input:
    [STATES] - q0 (precizare extra dacă este de start sau de sfarșit)
    [SIGMA] - simbol
    [GAMMA] - simbol stivă
    [RULES] - stare_src, symbol_input(sau eps), stack_pop(sau eps), stare_dest, stack_push(sau eps)
    [END] - marchează sfârșitul fiecărei secțiuni
"""

import sys

EPS = "ε"
DOLLAR = "$"

def load_pda(filename: str):
    # Citește liniile (fără comentarii / goluri)
    sections =  dict()
    with open(filename) as f:
        lines = [line.split('#', 1)[0].strip() for line in f if line.split('#', 1)[0].strip()]

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


    # STĂRI: listă, stare de start, stări finale
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

    # TRANZITII
    
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

    # veriicare prezenta sectiuni STATES, SIGMA SI RILES

    for req in ('states', 'sigma', 'gamma', 'rules'):
        if req not in pda:
            f"Missing [{req.upper()}] section!"

    return pda

def is_valid(word: str, pda, max_steps: int = 10000) -> bool:
    queue = [[pda['start'], 0, DOLLAR]]
    visited = [queue[0]]
    steps = 0

    while queue and steps < max_steps:
        # scoate primul element
        state, pos, stack = queue.pop(0)
        steps += 1

        # accepțare dacă a fost citit tot cuvântul și ește într-o stare finală
        if pos == len(word) and state in pda['finals']:
            return True

        top = stack[-1] if stack else EPS

        # parcurge toate regulile care pleacă din starea curentă
        for rule in pda['rules']:
            q_src, symbol_input, stack_pop, q_dest, push = rule
            if q_src != state:
                continue

            # potrivirea pe simbolul de intrare
            if symbol_input != EPS:
                if pos >= len(word) or word[pos] != symbol_input:
                    continue
                new_pos = pos + 1
            else:
                new_pos = pos

            # potrivirea pe vârful stivei
            if stack_pop != EPS and top != stack_pop:
                continue

            # construire stiva nouă
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
    pda = load_pda("a^n-b^n.pda")

    tests = ["", "ab", "aabb", "aaabbb", "aab", "abb"]
    for test in tests:
        print(f"{test}: {is_valid(test, pda)}")

    print()
    pda = load_pda("parentheses.pda")

    tests = ["", "()", "(())", "()()", "(()())", "(()", "())(", ")(()"]
    for test in tests:
        print(f"{test}: {is_valid(test, pda)}")

    print()

    # rulare pt argumente command line
    n = len(sys.argv)
    if n > 1:
        print()
        print('--- ARGUMENTE COMMAND LINE ---')
        for i in range(1, n):
            print(f"{sys.argv[i]}: {is_valid(sys.argv[i], pda)}")

if __name__ == "__main__":
    main()
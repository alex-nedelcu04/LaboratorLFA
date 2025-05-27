EPS = "ε"
def load_nfa(fn: str):
    nfa = {}
    with open(fn) as f:
        lines = [l.strip() for l in f if l.strip() and l.lstrip()[0] != '#']

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

    # prelucrare [STATES]
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

    for row in rule_rows:
        p, a, r = [x.strip() for x in row.split(',')]
        if a.lower() in ('eps', 'epsilon'):
            a = EPS
        nfa['rules'].append((p, a, r))

    return nfa

def epsilon_closure(states, rules):
    """Toate stările accesibile doar prin ε din oricare stare din 'states'."""
    stack = list(states)
    closure = set(states)
    while stack:
        q = stack.pop()
        for p, a, r in rules:
            if p == q and a == EPS and r not in closure:
                closure.add(r)
                stack.append(r)
    return list(closure)

def isValid(word, nfa):

    current = epsilon_closure({nfa['start']}, nfa['rules'])

    # parcurgere simboluri
    for sym in word:
        next_states = []

        for q in current:
            for p, a, r in nfa['rules']:
                if p == q and a == sym:
                    next_states.append(r)

        # Închidere ε peste stările nou atinse
        current = epsilon_closure(next_states, nfa['rules'])

        # Dacă nu mai există nicio ramură acceptabila -> respingere
        if not current:
            return False

    # Acceptare dacă oricare dintre stările curente este finală
    return any(q in nfa['finals'] for q in current)

nfa = load_nfa("automat.nfa")


words = ["", "0", "01", "001", "0011", "00110", "11001"]
for word in words:
    print(f"{word} -> {isValid(word, nfa)}")

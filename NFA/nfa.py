"""
Format fișier input:
   [STATES] - fiecare linie: nume_stare (precizare extra dacă este de start sau de sfârșit)
   [SIGMA] - alfabetul de intrare (un simbol pe linie)
   [RULES] - regulile de tranziție: stare_plecare, simbol, stare_sosire
   [END] - marchează sfârșitul fiecărei secțiuni
"""

EPS = "ε"
def load_nfa(fn: str):
    nfa = dict()
    # citire fișier și eliminare comentarii / linii goale
    with open(fn) as f:
        lines = [l.strip() for l in f if l.strip() and l.lstrip()[0] != '#']

    # extregere sectiuni

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

    # veriicare prezenta sectiuni STATES, SIGMA SI RILES

    for req in ('states', 'sigma', 'rules'):
        if req not in nfa:
            f"Missing [{req.upper()}] section!"

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

    for rule_line in rule_rows:
        src_state, input_symbol, dest_state = [field.strip() for field in rule_line.split(',')]

        if input_symbol.lower() in ('eps', 'epsilon'):
            input_symbol = EPS

        nfa['rules'].append((src_state, input_symbol, dest_state))

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

def isValid(test, nfa):

    current = epsilon_closure({nfa['start']}, nfa['rules'])

    # parcurgere simboluri
    for sym in test:
        next_states = []

        for q in current:
            for p, a, r in nfa['rules']:
                if p == q and a == sym:
                    next_states.append(r)

        #  închidere ε peste stările nou atinse
        current = epsilon_closure(next_states, nfa['rules'])

        # Dacă nu mai există nicio ramură acceptabila -> respingere
        if not current:
            return False

    # Acceptare dacă oricare dintre stările curente este finală
    return any(q in nfa['finals'] for q in current)

nfa = load_nfa("automat.nfa")


tests = ["", "0", "01", "001", "0011", "00110", "11001"]
for test in tests:
    print(f"{test}: {isValid(test, nfa)}")

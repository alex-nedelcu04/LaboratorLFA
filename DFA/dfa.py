"""
    Format fisier input:
       [STATES] – fiecare linie: nume_stare (precizare extra dacă este de start sau de sfarșit)
       [SIGMA] – alfabetul de intrare (un simbol pe linie)
       [RULES] – regulile de tranziție: stare_plecare, simbol, stare_sosire
       [END] – marchează sfârșitul fiecărei secțiuni
       Comentarii : //
"""

def load_dfa(fn: str):
    dfa = dict()
    with open(fn) as f:
        # citire fișier și eliminare comentarii / linii goale
        lines = [line.split("//", 1)[0].strip() for line in f if line.split("//", 1)[0].strip()]
        idx_line = 0
        num_lines = len(lines)
        while idx_line < num_lines:
            # parcurgere pana la intalnirea unuia dintre [STATES], [SIGMA] si [RULES]
            while lines[idx_line][0] != '[' and lines[idx_line][-1] != ']':
                idx_line += 1
            if lines[idx_line].upper() != '[END]':
                argument = lines[idx_line][1:-1].lower()
                idx_line += 1
                # parcurgere argumete primite pana la intalnirea unui [END]
                while lines[idx_line].upper() != '[END]':
                    if argument not in dfa.keys():
                        dfa[argument] = [lines[idx_line]]
                    else:
                        dfa[argument].append(lines[idx_line])

                    idx_line += 1

            idx_line += 1

    for req in ('states', 'sigma', 'rules'):
        if req not in dfa:
            print(f"Missing [{req.upper()}] section!")
            
    # prelucrarea datelor din [STATES] pentru a obtine starea de inceput si de sfarsit

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

    # prelucarea datelor din RULES pentru a putea verifica corectidunea datelor ulterior
    # ex.: 'q0, 0, q1'; => [q0, 0 , q1]

    for idx_rule in range(len(dfa["rules"])):
        dfa['rules'][idx_rule] = list(dfa['rules'][idx_rule].split(','))
        dfa['rules'][idx_rule] = [elem.strip() for elem in dfa['rules'][idx_rule]]

    # verificare corectitudinii regulii

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

def is_valid(word: str, dfa: dict) -> bool:

    current_state = dfa['start']
    for symbol in word:
        if symbol not in dfa['sigma']:
            raise ValueError(f"Simbolul '{symbol}' nu face parte din alfabetul DFA!")
        # cauta tranzitia corespunzatoare
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
    print("automat.dfa: ")
    dfa = load_dfa("automat.dfa")
    tests = ["", "0", "00", "1", "01", "001", "010", "0101", "0100", "0001110"]
    for test in tests:
        print(f"{test}: {is_valid(test, dfa)}")

if __name__ == "__main__":
    main()
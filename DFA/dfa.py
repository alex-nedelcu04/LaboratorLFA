"""
    Format fisier input:
       [STATES] - fiecare linie: nume_stare (precizare extra dacă este de start sau de sfarșit)
       [SIGMA] - alfabetul de intrare (un simbol pe linie)
       [RULES] - regulile de tranziție: stare_plecare, simbol, stare_sosire
       [END] - marchează sfârșitul fiecărei secțiuni
"""

def load_dfa(fn: str):
    dfa = dict()
    with open(fn) as f:
        # citire fișier și eliminare comentarii / linii goale
        lines = [line.strip() for line in f if line.strip() and not line.lstrip().startswith('#')]
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

"""
    Un joc în care DFA-ul reprezintă planul camerelor.
    level 1 -> terminare imediat după ajungerea în camera finală
    level = 2  -> trebuie luată o lingură din bucătărie înainte de a putea accesa camera finală
"""

def play_game(game_dfa: dict , level: int):
    current_room = game_dfa["start"]
    if level == 2:
        isSpoonEquiped = False

    while current_room != "Exit":
        if level == 2:
            # bucătăria conține lingura – este ridicată automat
            if current_room == 'Kitchen':
                print("Spoon equipped!")
                isSpoonEquiped = True

            if isSpoonEquiped == True:
                print("Spoon: Equipped")
            else:
                print("Spoon: Not equipped")

        print(f"Current room: {current_room}")
        # construirea listei direcțiilor posibile din camera curentă
        possible = [rule[1] for rule in game_dfa["rules"] if rule[0] == current_room]
        print("Possible directions:", ", ".join(possible))
        direction = input("Choose direction: ")

        if direction not in game_dfa["sigma"]:
            print()
            print("Not a valid direction")
            print()
            continue

        # căutare regulă (current_room, direction, ?)
        found_direction = False
        for rule in game_dfa["rules"]:
            if rule[0] == current_room:
                if rule[1] == direction:
                    found_direction = True
                    # s-a ajuns în camera finală
                    if rule[2] == game_dfa["F"]:
                        if level == 1:
                            current_room = rule[2]
                        elif level == 2:
                            if isSpoonEquiped == True:
                                current_room = rule[2]
                            else:
                                # continuare fără schimbarea camerei
                                print("Can't exit. Spoon is not equipped!")
                                continue
                    else:
                        current_room = rule[2]

                    break

        if found_direction == False:
            print(f"No rule for {direction} direction")

        print()
    print("Game over!")



# print(load_dfa("automat.dfa"))
game_dfa = load_dfa("game_level.dfa")
print(game_dfa)
play_game(game_dfa, 2)
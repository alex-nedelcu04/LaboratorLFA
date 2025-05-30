import re
def load_turing(fn: str) :
    turing = dict()
    found_start = False
    found_end = False
    with open(fn) as f:
        lines = [line.split('#', 1)[0].strip() for line in f if line.split('#', 1)[0].strip()]
        idx_line = 0
        num_lines = len(lines)
        while idx_line < num_lines:
            # parcurgere pana la intalnirea unuia dintre [STATES], [SIGMA] si [RULES]
            while lines[idx_line][0] != '[' and lines[idx_line][-1] != ']':
                idx_line += 1
            
            if lines[idx_line].upper() == '[STATES]':
                idx_line += 1
                # parcurgere argumete primite pana la intalnirea unui [END]
                while lines[idx_line].upper() != '[END]':
                    add_to_argument = [elem.strip() for elem in lines[idx_line].split(',')]
                    if add_to_argument[0] == 'space':
                        add_to_argument[0] = ' '

                    if len(add_to_argument) == 2 and add_to_argument[1] == 'start':
                         turing['start'] = add_to_argument[0]
                         found_start = True
                    elif len(add_to_argument) == 2 and add_to_argument[1] == 'end':
                        turing['end'] = add_to_argument[0]
                        found_end = True
                        
                    if 'states' not in turing.keys():
                        turing['states'] = [add_to_argument[0]]
                    else:
                        turing['states'].append(add_to_argument[0])
                    
                    idx_line += 1
            elif lines[idx_line].upper() != '[END]':
                argument = lines[idx_line][1:-1].lower()
                idx_line += 1
                # parcurgere argumete primite pana la intalnirea unui [END]
                while lines[idx_line].upper() != '[END]':
                    add_to_argument = lines[idx_line]
                    if add_to_argument == 'space':
                        add_to_argument = ' '
                    if argument not in turing.keys():
                        turing[argument] = [add_to_argument]
                    else:
                        turing[argument].append(add_to_argument)

                    idx_line += 1

            idx_line += 1

    # veriicare prezenta sectiuni STATES, SIGMA SI RULES

    for req in ('states', 'characters', 'directions', 'rules'):
        if req not in turing.keys():
            print(f"Missing [{req.upper()}] section!")
            return

    if found_start == False and found_end == False:
        print("No start state and no end state found!")
        return

    if found_start == False:
        print("No start state found!")
        return

    if found_end == False:
        print("No end state found!")
        return

    return turing


def run_turing(turing: dict, tape: list, tape_size = 1000):

    if type(turing) != dict:
        print("Didn't receive a turing configuration!")
        return

    if type(tape) != list or tape == []:
        tape = [' '] * tape_size
    head = 0
    states = turing["states"]
    characters = turing["characters"]
    directions = turing["directions"]
    rules = turing["rules"]

    current_state = turing['start']
    while head in range(tape_size) and current_state != turing['end']:
        rule_applied = False
        for rule in rules:
            # extragere informatii din reguli
            start, end = rule.split("->")

            start = start.replace('(', '').replace(')', '').strip()
            end = end.replace('(', '').replace(')', '').strip()

            start, end = start.split(','), end.split(',')

            start = [elem.strip() for elem in start]
            end = [elem.strip() for elem in end]
            if start[1] == "" or start[1] == "space":
                start[1] = ' '
            if end[1] == "" or end[1] == "space":
                end[1] = ' '


            # aplicare regula
            if current_state == start[0] and tape[head] == start[1]:
                current_state = end[0]
                tape[head] = end[1]
                if end[2] == 'L':
                    head -= 1
                elif end[2] == 'R':
                    head += 1
                rule_applied = True
                break

        if not rule_applied:
            break
    return tape

def main():
    tape_size = 1000
    for fn in ["write_12_then_stop.turing", "write_1010_then_stop.turing", "right_left_right_write_1.turing"]:
        tape = [' '] * tape_size
        print(f"{fn}:")
        tape = run_turing(load_turing(fn), tape, tape_size)
        print(tape)
        print()
    
    
    tape = [' '] * tape_size
    tape[0] = tape[1] = tape[2] = tape[3] = '1'
    print("add_1_to_existing_tape.turing:")
    print(f"Tape before: {tape}")
    tape = run_turing(load_turing("add_1_to_existing_tape.turing"), tape, tape_size)
    print(f"Tape now: {tape}")

if __name__ == "__main__":
    main()
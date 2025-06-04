"""
Input file format:
   [STATES] - on every line: state_name [, start] / [, end] (one state need to be labeled as start, another as end)
   [CHARACTERS] - input alphabet (one symbol per line)
   [DIRECTIONS] - all possible (L/R)
   [RULES] - transition rules: (source_state, symbol) -> (destination_state, symbol, direction)
   [END] - marks the end of a section
   Comments : #
"""
import sys

def load_turing(fn: str) :
    turing = dict()
    found_start = False
    found_end = False
    with open(fn, encoding='utf-8') as f:
        # read from file and ignore comments and empty lines
        lines = [line.split("#", 1)[0].strip() for line in f if line.split("#", 1)[0].strip()]
        idx_line = 0
        num_lines = len(lines)
        while idx_line < num_lines:
            # go through lines until reaching one of [STATES], [SIGMA] or [RULES]
            while lines[idx_line][0] != '[' and lines[idx_line][-1] != ']':
                idx_line += 1
            
            if lines[idx_line].upper() == '[STATES]':
                idx_line += 1
                # go through arguments until reaching [END]
                while lines[idx_line].upper() != '[END]':
                    # get states and store which the start and end ones
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
            elif lines[idx_line].upper() != '[END]': # Section that is not [STATES]
                argument = lines[idx_line][1:-1].lower()
                idx_line += 1
                # go through arguments until reaching [END]
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

    # verify if sections [STATES], [CHARCATERS], [DIRECTIONS] and [RULES] are all present

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
            # extract data from rules
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


            #  apply rule
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
    return ''.join(tape)

def convert_string_to_tape(tape_size: int, s = "") -> list:
    tape = [' ']*tape_size
    str_length = len(s)
    if str_length < tape_size:
        for idx in range(0, str_length):
            tape[idx] = s[idx]
    return tape
def main():
    tape_size = 80

    n = len(sys.argv)  # number of arguments

    # run command line arguments (if they exist)
    # Arguments: filename1 string1 filname2 string2
    if n > 1 and n % 2 != 0: # even -> arguments are not all (filename, string) pairs
        print('--- COMMAND LINE ARGUMENTS ---')
        for i in range(1, n, 2):

            print(f"{sys.argv[i]}:")
            tape = convert_string_to_tape(tape_size, sys.argv[i+1])
            print(f"Tape before: ({''.join(tape)})")
            tape = run_turing(load_turing(sys.argv[i]), tape, tape_size)
            print(f"Tape now: ({tape})")
            print()

    else:
        # default tests if not
        for fn in ["write_12_then_stop_TURING.txt", "write_1010_then_stop_TURING.txt",
                   "right_left_right_write_1_TURING.txt", "1_every_second_blank_TURING.txt"]:
            tape = [' '] * tape_size
            print(f"{fn}:")
            print(f"Tape before: ({''.join(tape)})")
            tape = run_turing(load_turing(fn), tape, tape_size)
            print(f"Tape now: ({tape})")
            print()

        tape = convert_string_to_tape(tape_size, "1111")
        print("add_1_to_existing_tape_TURING.txt:")
        print(f"Tape before: ({''.join(tape)})")
        tape = run_turing(load_turing("add_1_to_existing_tape_TURING.txt"), tape, tape_size)
        print(f"Tape now: ({tape})")

        tape = convert_string_to_tape(tape_size, "110110$        %           %    ")
        print("copy_string_between_%_TURING.txt:")
        print(f"Tape before: ({''.join(tape)})")
        tape = run_turing(load_turing("copy_string_between_%_TURING.txt"), tape, tape_size)
        print(f"Tape now: ({tape})")


if __name__ == "__main__":
    main()
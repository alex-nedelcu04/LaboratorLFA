from dfa import load_dfa
"""
    A game where a DFA is used to map the planning of multiple rooms
    level = 1 -> Game ends when you reach the "Exit" room
    level = 2  -> You need to equip a spoon from the Kitchen to be able to acces the "Exit" room
"""

def play_game(game_dfa: dict , level: int):
    current_room = game_dfa["start"]
    if level == 2:
        isSpoonEquiped = False

    while current_room != "Exit":
        if level == 2:
            # The kitchen include the spoon - it is picked up automaticallu
            if current_room == 'Kitchen':
                print("Spoon equipped!")
                print()
                isSpoonEquiped = True

            if isSpoonEquiped == True:
                print("Spoon: Equipped")
            else:
                print("Spoon: Not equipped")

        print(f"Current room: {current_room}")
        # creating the list of possible directions from the current room
        possible = [rule[1] for rule in game_dfa["rules"] if rule[0] == current_room]
        print("Possible directions:", ", ".join(possible))
        direction = input("Choose direction: ")

        if direction not in game_dfa["sigma"]:
            print()
            print("Not a valid direction!")
            print()
            continue

        # searching for the rule (current_room, direction, ?)
        found_direction = False
        for rule in game_dfa["rules"]:
            if rule[0] == current_room:
                if rule[1] == direction:
                    found_direction = True
                    # "Exit" room reached
                    if rule[2] == game_dfa["F"]:
                        if level == 1:
                            current_room = rule[2]
                        elif level == 2:
                            if isSpoonEquiped == True:
                                current_room = rule[2]
                            else:
                                # Spoon not equipped. Continue without changing rooms
                                print()
                                print("Can't exit. Spoon is not equipped!")
                                continue
                    else:
                        current_room = rule[2]

                    break

        if found_direction == False:
            print()
            print(f"No rule for {direction} direction!")

        print()
    print("Game over!")


def main():
    game_dfa = load_dfa("game_DFA.txt")
    # print(game_dfa)
    print("--> level = 1 - Game ends when you reach the Exit room")
    print("--> level = 2  - You need to equip a spoon from the Kitchen to be able to acces the Exit room")
    print()
    level = int(input("Enter the level you want to play: "))
    print("---- DFA ROOMS GAME ----")
    play_game(game_dfa, level)

if __name__ == "__main__":
    main()
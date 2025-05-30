from dfa import load_dfa
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


def main():
    # print(load_dfa("automat.dfa"))
    game_dfa = load_dfa("game_level.dfa")
    print(game_dfa)
    play_game(game_dfa, 2)

if __name__ == "__main__":
    main()
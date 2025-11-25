import random

def guess_number_game():
    print("გამარჯობა მეგობარო! შენი მიზანია სწორად გამოიცნო ჩემი ჩაფიქრებული რიცხვი ❤️")

    while True:
        while True:
            name = input("ჩაწერე შენი სახელი: ")
            if name == "":
                print("სახელი ცარიელი ვერ იქნება. სცადე თავიდან.\n")
            else:
                break

        print(f"\n{name}! მოდი დავიწყოთ თამაში.\n")

        min_range = 1

        while True:
            max_input = input("შეიყვანე გამოსაცნობი რიცხვების დიაპაზონის მაქსიმალური რიცხვი: ")

            if not max_input.isdigit():
                print("გთხოვ, შეიყვანე მხოლოდ ნატურალური რიცხვები!\n")
                continue

            max_range = int(max_input)

            if max_range <= 0:
                print("გთხოვ შეიყვანე 1-ზე მეტი რიცხვი!\n")
                continue

            break

        secret = random.randint(min_range, max_range)
        range_size = max_range - min_range + 1

        attempts = 0
        power = 1
        while power < range_size:
            power *= 2
            attempts += 1

        print(f"\n{name}, შენ აირჩიე დიაპაზონი: {min_range}–დან {max_range}–მდე.")
        print(f"გაქვს {attempts} ცდა. წარმატებები!\n")

        current_attempts = attempts
        while current_attempts > 0:
            print(f"დარჩენილი ცდების რაოდენობა: {current_attempts}")
            guess_input = input("მე ვფიქრობ რომ ჩაფიქრებული რიცხვია: ")

            if not guess_input.isdigit():
                print("მხოლოდ ნატურალური რიცხვები!😉\n")
                continue

            guess = int(guess_input)

            if guess < min_range or guess > max_range:
                print("რიცხვი მითითებულ დიაპაზონში უნდა იყოს!\n")
                continue

            if guess == secret:
                print(f"\nგილოცავ, {name}! შენ გამოიცანი - {secret}! 🎉\n")
                break
            elif guess < secret:
                print("ჩემი ჩაფიქრებული რიცხვი უფრო დიდია. 😴\n")
            else:
                print("ჩემი ჩაფიქრებული რიცხვი უფრო პატარაა. 😏\n")

            current_attempts -= 1
        else:
            print(f"\n{name}, შენ დამარცხდი! ჩემი ჩაფიქრებული რიცხვი იყო {secret}.\n")

        replay = input("გინდა თავიდან თამაში? (კი/არა): ")
        if replay != 'კი':
            print("\nმადლობა თამაშისთვის! 😉")
            break
        if replay != 'არა':
            exit

guess_number_game()

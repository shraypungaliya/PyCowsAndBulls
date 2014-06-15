from cows_bulls_game import CowsAndBullsGame
import sys


def play():
    print("\nWelcome to Cows and Bulls.")
    difficulty = _get_difficulty()
    total_guesses = 10
    print("You have " + str(total_guesses) + " guess(es) to find my " + str(difficulty[1] + 2) + " letter word.")
    game = CowsAndBullsGame(total_guesses = total_guesses, difficulty = difficulty)
    while True:
        guess = str(raw_input("\nWhat is your guess?: "))
        guess_result = game.try_guess(guess)
        if guess == "11235":
            if _secret_code(game) == False:
                continue
        elif guess_result["game_status"] == "won":
            print("\nCongratulations! You guessed my word.")
            _play_again()
        elif guess_result["game_status"] == "lost":
            print("\nSorry! You didn't guess my word. My word was '%s'" % game._final_word)
            _play_again()
        elif guess_result["game_status"] == "in_play":
            if guess_result["try_status"] == "accepted":
                print ("Guess " + str(guess_result["tries_used"]) + "/" + str(total_guesses) + ": The word " + guess + " has: \n\n" + str(guess_result["cows"]) + " cows \n" + str(guess_result["bulls"]) + " bulls")
            else:
                reject_statements(game, guess)

def _get_difficulty():
    print("")
    while True:
        try:
            difficulty = int(raw_input("Please choose a difficulty (1, 2, or 3): "))
            if difficulty == 1:
                return ("easy",1)
            elif difficulty == 2:
                return "medium",2
            elif int(difficulty) == 3:
                return "hard",3
            elif difficulty == 11235:
                if not _secret_code():
                    continue
            else:
                print("Sorry, that number is invalid. Please try again.")
        except ValueError:
            print("Please enter a number (1-3).")

def reject_statements(game, guess):
    guess_reject_reason_ = game.try_guess(guess)["reject_reason"]
    if guess_reject_reason_ == "exceeded_length_error":
        print("Your word should be %s letters long. Please try again." % game.get_length_guess())
    elif guess_reject_reason_ == "repeated_letter_error":
        print("Your word has a repeated letter. Please try again.")
    elif guess_reject_reason_== "word_previously_guessed":
        print("You have already guessed that word. Please try again.")
    elif guess_reject_reason_== "empty_guess_error":
        print("Please enter a word. Please try again.")
    elif guess_reject_reason_== "multiple_word_error":
        print("Please enter only one word. Please try again.")
    elif guess_reject_reason_ == "not_a_word":
        print("'%s' is not a word in the dictionary. Please try again."  % guess)
    else:
        print("Sorry, I don't know what that means. Please try again.")

def _play_again():
    while True:
        try:
            play_again = raw_input("\nWould you like to play again?: ").lower().split()[0]
        except:
            print("That answer is invalid. Please try again.")
        if play_again == "yes" or play_again == "y":
            play()
        elif play_again == "no" or play_again == "n":
            sys.exit()
        else:
            print("Please answer 'y' or 'n'")


def _secret_code(game = 0):
    execute = raw_input("What would you like to do?: ")
    if execute.lower() == "word":
        print(game._final_word)
        return True
    elif execute.lower() == "end":
        sys.exit()
    elif execute.lower() == "play again" or execute.lower() == "reset":
        _play_again()
    elif execute.lower() == "add tries":
        try:
            added_tries = int(raw_input("How many tries would you like to add?: "))
            game.add_tries(added_tries)
        except:
            print("Sorry, that command is currently invalid.")
    else:
        return False
play()


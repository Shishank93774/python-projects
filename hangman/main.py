from words import words
import random


# ANSI escape codes for text colors
class TextColor:
    RESET = "\033[0m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"


# Function to print colored text
def print_colored(text, color):
    print(f"{color}{text}{TextColor.RESET}")


def get_valid_word():
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word


def play_hangman(lives = 6):
    chosen_word = get_valid_word()
    guess_set = set(chosen_word)
    user_set = set()
    while len(guess_set) > 0 and lives > 0:
        print("Already chosen letters: ", end="")
        for _ in user_set:
            print(_, end=" ")
        print()
        for i in range(0, len(chosen_word)):
            if chosen_word[i] in user_set:
                print(chosen_word[i], end="")
            else:
                print("-", end="")
        print()
        print(f"You have {lives} live(s)")
        ch = input("Guess a letter: ")

        if ch in user_set:
            print_colored("You already have guessed it, please try again.", TextColor.YELLOW)
        elif ch in guess_set:
            guess_set.remove(ch)
            user_set.add(ch)
            print_colored("Correct guess", TextColor.GREEN)
        else:
            user_set.add(ch)
            print_colored("Incorrect guess, please try again", TextColor.RED)
            lives -= 1

    if lives == 0:
        print("You lost :(")
    else:
        print("Yayy!, you won :)")

    print("The correct word was: ", chosen_word)


play_hangman(6)
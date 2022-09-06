from pathlib import Path
import ascii_art
from time import sleep
import os

# Required functions
def check_win(secret_word: str, old_letters_guessed: list[str]) -> bool:
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False

    return True

def show_hidden_word(secret_word: str, old_letters_guessed: list[str]) -> str:
    return " ".join([letter if letter in old_letters_guessed else "_" for letter in secret_word])
 
def check_valid_input(letter_guessed: str, old_letters_guessed: list[str]) -> bool:
    return len(letter_guessed) == 1 and letter_guessed.isalpha and letter_guessed not in old_letters_guessed

def try_update_letter_guessed(letter_guessed: str, old_letters_guessed: list[str]) -> bool:
    is_valid = check_valid_input(letter_guessed, old_letters_guessed)

    if is_valid:
        old_letters_guessed.append(letter_guessed)
    else:
        print(f"Bad input: {letter_guessed}\nGuessed letters: {' -> '.join(old_letters_guessed)}")

    return is_valid

def choose_word(file_path: str, index: int) -> str:
    with open(file_path, "r") as f:
        return f.read().split(" ")[index]

# My own functions
def file_chooser() -> str | None:
    return input("Enter a file path containing the words: ")

def clear() -> None:
    os.system('clear')

def render(secret_word: str, old_letters_guessed: list[str], tries: int) -> None:
    clear()
    print(ascii_art.stages[tries])
    print(show_hidden_word(secret_word, old_letters_guessed))

def main() -> None:
    MAX_TRIES = 6


    while True:
        file_path = file_chooser()

        if file_path is not None and Path(file_path).exists():
            break

        print("Unknown file.")

    while True:
        word_index = input("Enter the location of a word: ")

        try:
            word_index = int(word_index)
            break
        except:
            print("Not a number.")

    
    secret_word = choose_word(file_path, word_index)
    old_letters_guessed = []
    num_of_tries = 0

    print(f"Secret word: {secret_word}")

    sleep(2)
    clear()

    render(secret_word, old_letters_guessed, num_of_tries)
    while num_of_tries < MAX_TRIES:
        while True:
            letter = input("Guess a letter: ").lower()
            if try_update_letter_guessed(letter, old_letters_guessed):
                break
            else:
                print()

        if check_win(secret_word, old_letters_guessed):
            render(secret_word, old_letters_guessed, num_of_tries)
            print("You won!")
            return

        is_correct = letter not in secret_word

        if is_correct:
            num_of_tries += 1

        render(secret_word, old_letters_guessed, num_of_tries)

        if is_correct:
            print(f"The letter {letter} is not in the word :(")
        else:
            print(f"The letter {letter} is in the word :)")

    print("You lost...")


        

if __name__ == "__main__":
    main()


from pathlib import Path
import ascii_art
from time import sleep
import os
from typing import Tuple

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

def try_update_letter_guessed(letter_guessed: str, old_letters_guessed: list[str]) -> Tuple[bool, str]:
    is_valid = check_valid_input(letter_guessed, old_letters_guessed)

    if is_valid:
        old_letters_guessed.append(letter_guessed)
    else:
        return is_valid, f"Bad input: {letter_guessed}\nGuessed letters: {' -> '.join(old_letters_guessed)}"

    return is_valid, ""

# My own functions
def clear() -> None:
    os.system('clear')

def render_hangman(secret_word: str, old_letters_guessed: list[str], tries: int, max_tries: int) -> None:
    clear()
    print(ascii_art.stages[tries])
    print(show_hidden_word(secret_word, old_letters_guessed))
    print(f"Tries left: {max_tries-tries}")

def game_loop() -> None:
    MAX_TRIES = 6
    clear()
    print(ascii_art.opening)

    while True:
        file_path = input("Enter a file path containing the words: ")
    
        if file_path is not None and Path(file_path).exists():
            break
    
        print("Unknown file.")
    
    with open(file_path, "r") as f:
        words = f.read().split(" ")
    
    while True:
        word_index = input("Enter the location of a word: ")
    
        try:
            word_index = int(word_index)
            secret_word = words[word_index].strip()
            break
        except IndexError:
            print("Overflow error.")
        except ValueError:
            print("Not a number.")

    old_letters_guessed = []
    num_of_tries = 0

    print(f"Secret word: {secret_word}")

    sleep(2)
    clear()

    render = lambda: render_hangman(secret_word, old_letters_guessed, num_of_tries, MAX_TRIES)
    render()

    while num_of_tries < MAX_TRIES:
        while True:
            letter = input("Guess a letter: ").lower()
            is_valid, error_msg = try_update_letter_guessed(letter, old_letters_guessed)
            if is_valid:
                break
            else:
                render()
                print(error_msg)

        if check_win(secret_word, old_letters_guessed):
            render()
            print("You won!")
            print(f"The word was: {secret_word}")
            return

        is_correct = letter in secret_word

        if is_correct:
            render()
            print(f"The letter {letter} is in the word :)")
        else:
            num_of_tries += 1
            render()
            print(f"The letter {letter} is not in the word :(")

    print("You lost...")
    print(f"The word was: {secret_word}")

def main() -> None:
    while True:
        game_loop()

        if (input("Play again? (Y/n): ") == "n"):
            break

if __name__ == "__main__":
    main()


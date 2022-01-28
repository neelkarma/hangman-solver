from functools import cache
import re
from typing import Counter


@cache
def getAllWords():
    with open("./english-words/words_alpha.txt", "r") as words_file:
        return [word.strip() for word in words_file.readlines()]


@cache
def getWordsOfLength(length: int):
    words = getAllWords()
    return list(filter(lambda word: length == len(word), words))


def getMostCommonCharsOf(words: list[str]) -> list[str]:
    return [
        item[0]
        for item in sorted(
            [[char, freq] for char, freq in Counter("".join(words)).items()],
            key=lambda item: item[1],
            reverse=True,
        )
    ]  # type: ignore


@cache
def getMostCommonCharsAll():
    return getMostCommonCharsOf(getAllWords())


def getWordScore(word: str):
    common_chars = getMostCommonCharsAll()
    score_mapping = {char: i + 1 for i, char in enumerate(reversed(common_chars))}

    score = 0
    for char in word:
        score += score_mapping[char]
    return score


def findPossibleWords(pattern: str, incorrect_guesses: set[str]):
    words = getWordsOfLength(len(pattern))

    def filterFunc(word: str):
        for guess in incorrect_guesses:
            if guess in word:
                return False
        for i, char in enumerate(pattern):
            if char == " ":
                continue
            if not char == word[i]:
                return False
        return True

    return sorted(filter(filterFunc, words), key=getWordScore, reverse=True)


def main():
    hangman_input = input("Enter a word: ").strip().lower()

    if re.search(r"[^a-z]", hangman_input):
        print("The word can only contain letters (no numbers or special characters).")
        return

    len_words = getWordsOfLength(len(hangman_input))
    guesses = getMostCommonCharsOf(len_words) if len_words else getMostCommonCharsAll()

    incorrect_guesses: set[str] = set()
    word_status = {char: False for char in set(hangman_input)}
    turns = 0

    def printHangmanStatus():
        print(
            f"""
{" ".join(char.upper() if word_status[char] else "_" for char in hangman_input)} 
{turns} turns taken
Incorrect Guesses: {", ".join(incorrect_guesses)}
Similar Words: {", ".join(findPossibleWords("".join(char if word_status[char] else " " for char in hangman_input), incorrect_guesses))}

---
"""
        )

    printHangmanStatus()

    for guess in guesses:
        if guess in hangman_input:
            word_status[guess] = True
        else:
            incorrect_guesses.add(guess)
            turns += 1
        printHangmanStatus()
        if all(word_status.values()):
            print("WIN")
            break


if __name__ == "__main__":
    main()

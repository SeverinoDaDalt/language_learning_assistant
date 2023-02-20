import random
from words import Word
from utils import ask_user, keyboard_adapter
from typing import List


def ask_spanish_translation(word: Word, reverse: bool = False):
    correct_result = True
    guessed_target_spellings = set()
    if reverse:
        origin_language = "pinyin"
        origin_spelling = random.choice(word.pinyin_spelling)
        target_language = "spanish"
        target_spellings = set(word.spanish_spelling.copy())
    else:
        origin_language = "spanish"
        origin_spelling = random.choice(word.spanish_spelling)
        target_language = "pinyin"
        target_spellings = set(word.pinyin_spelling.copy())
    prompt = f"Translate the following word from {origin_language} to {target_language}: {origin_spelling}"
    response = None  # just to make pycharm happy
    while target_spellings != guessed_target_spellings and correct_result:
        response = keyboard_adapter(ask_user(prompt))
        # todo: check if already given
        if response in guessed_target_spellings:
            print("Translation already given, try another one.")
        elif response not in target_spellings:
            correct_result = False
            if response == "!solution":
                print(f"The possible translations were {target_spellings}")
            else:
                print("Wrong answer. (Next time, if you want to be given the solution, type '!solution')")
        else:
            guessed_target_spellings.add(response)
            print("Right answer!")
        prompt = f"There are more translations for the word {origin_spelling}. " + \
                 (f"(you already guessed {guessed_target_spellings})" if guessed_target_spellings else "")
    if correct_result:
        result = "correct"
        word.update_attempts(1)
        interaction = f"Fully correct translation for word {word}."
    elif response == "!solution":
        result = "helped"
        word.update_attempts(-1)
        interaction = f"Help was required with the translation of word {word}" + \
                      (f" after correctly guessing {guessed_target_spellings}" if guessed_target_spellings else "") + \
                      "."
    else:
        result = "wrong"
        word.update_attempts(-1)
        interaction = f"Wrong translation ({response}) of word {word} was given" + \
                      (f" after correctly guessing {guessed_target_spellings}" if guessed_target_spellings else "") + \
                      "."
    return (interaction, 2), result


def exhaustive_training(words: List[Word]):
    interactions = []
    random.shuffle(words)
    results = []
    for word in words:
        interaction, result = ask_spanish_translation(word)
        interactions.append(interaction)
        results.append(result)
    correct = results.count("correct")
    wrong = results.count("helped") + results.count("wrong")
    prompt = f"Correctly guessed {correct} words out of {wrong + correct}."
    print(prompt)
    interactions.append((prompt, 2))
    return interactions

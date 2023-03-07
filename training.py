import random
from words import Word
from utils import ask_user, keyboard_adapter
from typing import List
import prompts


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
    prompt = prompts.ASK_TRANSLATION(origin_language, target_language, origin_spelling)
    response = None  # just to make pycharm happy
    while target_spellings != guessed_target_spellings and correct_result:
        response = keyboard_adapter(ask_user(prompt))
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
        prompt = prompts.ASK_ANOTHER_TRANSLATION(origin_spelling, guessed_target_spellings)
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


def random_commentary(commentaries, probability=0.1):
    if commentaries and random.random() < probability:
        return random.choice(commentaries)
    return None


def exhaustive_training(words: List[Word], commentaries: List[str]):
    # training parameters
    do_shuffle = True
    commentaries_probability = 0.1
    repetitive_tags = {"día de la semana", "mes"}
    # begin training
    if do_shuffle:
        random.shuffle(words)
    interactions = []
    wrong = []
    helped = []
    correct = []
    repeated_tags = set()
    for word in words:
        # check if word should be skipped
        repeated = False
        possible_repeated_tags = set()
        if word.tags:
            for tag in word.tags:
                if tag in repetitive_tags:
                    if tag in repeated_tags:
                        repeated = True
                        break
                    possible_repeated_tags.add(tag)
        if repeated:
            continue
        repeated_tags = repeated_tags | possible_repeated_tags
        # ask word
        interaction, result = ask_spanish_translation(word)
        interactions.append(interaction)
        if result == "wrong":
            wrong.append(word)
        elif result == "helped":
            helped.append(word)
        elif result == "correct":
            correct.append(word)
        commentary = random_commentary(commentaries, probability=commentaries_probability)
        if commentary is not None:
            print(f"\nQUICK NOTE:\n{commentary}\n")
            commentaries.remove(commentary)
    # resume
    prompt = f"Correctly guessed {len(correct)} words out of {len(correct) + len(wrong) + len(helped)}."
    print(prompt)
    if not wrong + helped:
        print("PERFECT SCORE!")
    if wrong:
        print(f"You missed the following words:")
        for word in wrong:
            print(f" - {word}")
    if helped:
        print(f"You asked for help for the following words:")
        for word in helped:
            print(f" - {word}")
    # return progress
    interactions.append((prompt, 2))
    return interactions

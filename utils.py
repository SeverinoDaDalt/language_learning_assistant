from typing import Union, List
from config import USERNAME


seveyin_settings = {
    "a/-": "ā",
    "e/-": "ē",
    "i/-": "ī",
    "o/-": "ō",
    "u/-": "ū",
    "a/v": "ǎ",
    "e/v": "ě",
    "i/v": "ǐ",
    "o/v": "ǒ",
    "u/v": "ǔ",
}


def keyboard_adapter(seveyin_word: Union[str, List[str]]):
    seveyin_words = seveyin_word if type(seveyin_word) is list else [seveyin_word]
    pinyin_words = []
    for seveyin_word in seveyin_words:
        pinyin_word = seveyin_word
        for seveyin_character, pinyin_character in seveyin_settings.items():
            pinyin_word = pinyin_word.replace(seveyin_character, pinyin_character)
        pinyin_words.append(pinyin_word)
    return pinyin_words if len(pinyin_words) > 1 else pinyin_words[0]


def read_from_user(prompt: str = None, strip=True):
    response = None
    while response is None:
        try:
            response = input(prompt)
            if strip:
                response = response.strip()
            return response
        except UnicodeDecodeError:
            print(f"ERROR (UnicodeDecodeError). Try typing again carefully.")


def ask_user(prompt: str = None, valid_responses: List = None):
    if prompt is not None:
        print(prompt)
    response = read_from_user(f"{USERNAME}: ")
    if not valid_responses:
        return response
    while response not in valid_responses:
        print(f"Invalid option. Response must be one of {valid_responses}. Try again.")
        response = read_from_user(f"{USERNAME}: ")
    return response

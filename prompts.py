MAIN_MENU = """

What would you like to do:
 1- Add words to the dictionary.
 2- Remove a word from the dictionary.
 3- Show dictionary.
 4- Train.
 5- Exit.
 6- Debug mode.
"""

ADD_WORD = """Which word do you want to add? 
Expected format: chinese_spelling1,...chinese_spellingN;spanish_spelling1,...,spanish_spellingN;tag1,...,tagN. 
You can go on until you type 'exit'."""

SEARCH_WORD = f"What is the id of the word?"
CONFIRM_REMOVE = lambda word: f"Is this the word you want to delete? {word}. (y/n)"

DEBUG_MODE_ASK_DESCRIPTION = "Do you want to leave a description of what you have done?"
DEBUG_MODE_DESCRIPTION = "Please, do so down below."

SAVE_SESSION = "Do you want to save the session and all changes that were made to the dictionary? (y/n)"

ASK_TRANSLATION = lambda origin_language, target_language, origin_spelling: \
    f"Translate the following word from {origin_language} to {target_language}: {origin_spelling}"
ASK_ANOTHER_TRANSLATION = lambda origin_spelling, guessed_target_spellings: \
    f"There are more translations for the word {origin_spelling}. " + \
    (f"(you already guessed {guessed_target_spellings})" if guessed_target_spellings else "")


import datetime
from words import Dictionary
import os
import pickle
from config import SESSIONS_DIRECTORY, DICTIONARY
from utils import ask_user, keyboard_adapter
from training import exhaustive_training


class Session:
    def __init__(self):
        self.start = datetime.datetime.now()
        self.interactions = []
        # Load dictionary
        if os.path.exists(DICTIONARY):
            with open(DICTIONARY, "rb") as f_dic:
                self.dictionary = pickle.load(f_dic)
        else:
            prompt = f"The selected dictionary ({DICTIONARY}) does not exist yet. Do you want to initialize it? (y/n)"
            response = ask_user(prompt, valid_responses=["y", "n"])
            if response == "n":
                return
            self.dictionary = Dictionary([])

    def write_session(self):
        session_file = str(self.start).replace(" ", "_") + ".txt"
        with open(os.path.join(SESSIONS_DIRECTORY, session_file), "w") as f_session:
            for level, interaction in self.interactions:
                f_session.write("\t"*level + interaction + "\n")

    def add_interaction(self, interaction: str, level: int = 0):
        self.interactions.append((level, interaction))

    def run(self):
        # todo: create functions for options in session
        print(f"NEW SESSION STARTED ({self.start})")
        self.add_interaction(f"Beginning of session {self.start}")
        while True:
            prompt = \
"""
\nWhat would you like to do:
 1- Add words to the dictionary.
 2- Remove a word from the dictionary.
 3- Show dictionary.
 4- Train.
 5- Exit.
"""
            response = ask_user(prompt, valid_responses=["1", "2", "3", "4", "5"])
            if response == "5":
                break
            elif response == "1":
                self.add_interaction(f"Adding words", 1)
                prompt = "Which word do you want to add?\n Expected format: chinese_spelling1,...chinese_spellingN;" \
                         "spanish_spelling1,...,spanish_spellingN;tag1,...,tagN.\n You can go on until you type 'exit'."
                response = ask_user(prompt)
                while response != "exit":
                    aux = response.split(";")
                    if len(aux) == 2:
                        pinyin_spelling = keyboard_adapter(aux[0].split(","))
                        spanish_spelling = keyboard_adapter(aux[1].split(","))
                        word = self.dictionary.add_word(pinyin_spelling, spanish_spelling)
                        self.add_interaction(f"{word}", 2)
                    elif len(aux) == 3:
                        pinyin_spelling = keyboard_adapter(aux[0].split(","))
                        spanish_spelling = keyboard_adapter(aux[1].split(","))
                        tags = aux[2].split(",")
                        word = self.dictionary.add_word(pinyin_spelling, spanish_spelling, tags=tags)
                        self.add_interaction(f"{word}", 2)
                    else:
                        print("Wrong format!")
                        continue
                    response = ask_user()
                self.add_interaction(f"No more words", 2)
            elif response == "2":
                response = ask_user(f"What is the id of the word?")
                try:
                    response = int(response)
                except Exception:
                    print("The id must be an integer!")
                    continue
                word = self.dictionary.get_word_by_id(response)
                if word is None:
                    print("Word not found")
                    continue
                response = ask_user(f"Is this the word you want to delete? {word}. (y/n)", valid_responses=["y", "n"])
                if response == "y":
                    self.dictionary.remove_word_by_id(word.id_)
                    self.add_interaction(f"Word removed: {word}", 1)
                else:
                    print("The word was not removed.")
            elif response == "3":
                print("These are the words in the dictionary:")
                for word in self.dictionary.words:
                    print(f" - {word}")
                self.add_interaction(f"Checked dictionary", 1)
            elif response == "4":
                self.add_interaction(f"Start training.", 1)
                new_interactions = exhaustive_training(self.dictionary.words)
                for interaction, level in new_interactions:  # todo: instead of this update add_interaction func
                    self.add_interaction(interaction, level)
                print(f"Training session finished!")
            else:
                raise ValueError
        print("Session ended!")
        self.add_interaction(f"Session finished at {datetime.datetime.now()}")
        response = ask_user("Do you want to save the session and all changes that were made to the dictionary? (y/n)",
                            valid_responses=["y", "n"])
        if response == "y":
            print(f"Saving session ...")
            self.write_session()
            with open(DICTIONARY, "wb") as f_dic:
                print("Saving dictionary ...")
                pickle.dump(self.dictionary, f_dic)
            print("All changes were saved!")


def main():
    session = Session()
    session.run()


if __name__ == "__main__":
    main()

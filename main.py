import datetime
import pdb
from words import Dictionary
import os
import pickle
from config import SESSIONS_DIRECTORY, DICTIONARY
from utils import ask_user, keyboard_adapter, strip_list, load_commentaries
from training import exhaustive_training
import prompts
from typing import List, Union


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

    def add_interaction(self, interactions: Union[str, List[str]], level: int = 0):
        if type(interactions) is list:
            for interaction, new_level in interactions:
                self.interactions.append((new_level, interaction))
        else:
            self.interactions.append((level, interactions))

    # MENU OPTIONS
    def add_words(self):
        self.add_interaction(f"Adding words", 1)
        response = ask_user(prompts.ADD_WORD)
        while response != "exit":
            aux = response.split(";")
            if len(aux) == 2:
                pinyin_spelling = strip_list(keyboard_adapter(aux[0].split(",")))
                spanish_spelling = strip_list(keyboard_adapter(aux[1].split(",")))
                word = self.dictionary.add_word(pinyin_spelling, spanish_spelling)
                self.add_interaction(f"{word}", 2)
            elif len(aux) == 3:
                pinyin_spelling = strip_list(keyboard_adapter(aux[0].split(",")))
                spanish_spelling = strip_list(keyboard_adapter(aux[1].split(",")))
                tags = strip_list(aux[2].split(","))
                word = self.dictionary.add_word(pinyin_spelling, spanish_spelling, tags=tags)
                self.add_interaction(f"{word}", 2)
            else:
                print("Wrong format!")
            response = ask_user()
        self.add_interaction(f"No more words", 2)

    def search_and_or_remove_word(self):
        response = ask_user(prompts.SEARCH_WORD)
        try:
            response = int(response)
        except Exception:
            print("The id must be an integer!")
            return
        word = self.dictionary.get_word_by_id(response)
        if word is None:
            print("Word not found")
            return
        response = ask_user(prompts.CONFIRM_REMOVE(word), valid_responses=["y", "n"])
        if response == "y":
            self.dictionary.remove_word_by_id(word.id_)
            self.add_interaction(f"Word removed: {word}", 1)
        else:
            print("The word was not removed.")

    def show_dictionary(self):
        print("These are the words in the dictionary:")
        for word in self.dictionary.words:
            print(f" - {word}")
        self.add_interaction(f"Checked dictionary", 1)

    def train(self):
        self.add_interaction(f"Start training.", 1)
        commentaries = load_commentaries()
        new_interactions = exhaustive_training(self.dictionary.words, commentaries)
        self.add_interaction(new_interactions)
        print(f"Training session finished!")

    def exit(self):
        print("DEBUG MODE! (When you are done type 'continue')")
        self.add_interaction(f"Entered debug mode at {datetime.datetime.now()}", 1)
        pdb.set_trace()
        need_description = ask_user(prompts.DEBUG_MODE_ASK_DESCRIPTION, valid_responses=["y", "n"])
        if need_description == "y":
            debug_description = ask_user(prompts.DEBUG_MODE_DESCRIPTION)
            self.add_interaction(f"Commentary: {debug_description}", 2)
        self.add_interaction(f"Exited debug mode at {datetime.datetime.now()}", 1)

    def save_session(self):
        print(f"Saving session ...")
        self.write_session()
        with open(DICTIONARY, "wb") as f_dic:
            print("Saving dictionary ...")
            pickle.dump(self.dictionary, f_dic)
        print("All changes were saved!")

    def run(self):
        print(f"NEW SESSION STARTED ({self.start})")
        self.add_interaction(f"Beginning of session {self.start}")
        while True:
            response = ask_user(prompts.MAIN_MENU, valid_responses=["1", "2", "3", "4", "5", "6"])
            if response == "5":
                break
            elif response == "1":
                self.add_words()
            elif response == "2":
                self.search_and_or_remove_word()
            elif response == "3":
                self.show_dictionary()
            elif response == "4":
                self.train()
            elif response == "6":
                self.exit()
            else:
                raise ValueError
        print("Session ended!")
        self.add_interaction(f"Session finished at {datetime.datetime.now()}")
        response = ask_user(prompts.SAVE_SESSION, valid_responses=["y", "n"])
        if response == "y":
            self.save_session()


def main():
    session = Session()
    session.run()


if __name__ == "__main__":
    main()

from typing import Union, List


class Word:
    def __init__(self,
                 id_: int,
                 pinyin_spelling: Union[str, List[str]],
                 spanish_spelling: Union[str, List[str]],
                 tags: Union[str, List[str]] = None):
        self.id_ = id_
        self.pinyin_spelling = pinyin_spelling if type(pinyin_spelling) is list else [pinyin_spelling]
        self.spanish_spelling = spanish_spelling if type(spanish_spelling) is list else [spanish_spelling]
        self.tags = tags if tags is None or type(tags) is list else [tags]
        self.attempts = 0
        self.hits = 0
        self.fails = 0
        self.consecutive = 0  # if positive, consecutive hits. If negative, consecutive fails

    def __repr__(self):
        return f"id_: {self.id_}, pinyin_spelling: {self.pinyin_spelling}, spanish_spelling: {self.spanish_spelling}," \
               f" tags: {self.tags}"

    def represent_all_stats(self):
        return f"id_: {self.id_}, pinyin_spelling: {self.pinyin_spelling}, " \
               f"spanish_spelling: {self.spanish_spelling}, tags: {self.tags}, attempts: {self.attempts}, " \
               f"hits: {self.hits}, fails: {self.fails}, consecutive: {self.consecutive}"

    def add_pinyin_spelling(self, new_pinyin_spelling: Union[str, List[str]], replace: bool = False):
        if replace:
            self.pinyin_spelling = new_pinyin_spelling if type(new_pinyin_spelling) is list else [new_pinyin_spelling]
        else:
            self.pinyin_spelling.extend(new_pinyin_spelling if type(new_pinyin_spelling) is list
                                        else [new_pinyin_spelling])

    def add_spanish_spelling(self, new_spanish_spelling: Union[str, List[str]], replace: bool = False):
        if replace:
            self.spanish_spelling = new_spanish_spelling if type(new_spanish_spelling) is list \
                else [new_spanish_spelling]
        else:
            self.spanish_spelling.extend(new_spanish_spelling if type(new_spanish_spelling) is list
                                         else [new_spanish_spelling])

    def add_tag(self, new_tag: Union[str, List[str]], replace: bool = False):
        if replace:
            self.tags = new_tag if new_tag is None or type(new_tag) is list else [new_tag]
        else:
            self.tags.extend(new_tag if new_tag is None or type(new_tag) is list else [new_tag])

    def update_attempts(self, result: int):
        self.attempts += 1
        if result > 0:
            self.hits += 1
            if self.consecutive >= 0:
                self.consecutive += 1
            else:
                self.consecutive = 1
        elif result < 0:
            self.fails += 1
            if self.consecutive <= 0:
                self.consecutive -= 1
            else:
                self.consecutive = -1


class Dictionary:
    def __init__(self, words: List[Word]):
        self.words = words
        self.first_available_id = 0

    def add_word(self,
                 pinyin_spelling: Union[str, List[str]],
                 spanish_spelling: Union[str, List[str]],
                 tags: Union[str, List[str]] = None):
        word = Word(self.first_available_id, pinyin_spelling, spanish_spelling, tags)
        self.first_available_id += 1
        self.words.append(word)
        print(f"Added word to the dictionary: {word}")
        return word

    def get_word_by_id(self, id_: int):
        for word in self.words:
            if word.id_ == id_:
                return word
        return None

    def remove_word_by_id(self, id_: int):
        word = self.get_word_by_id(id_)
        self.words.remove(word)
        print(f"The following word was removed: {word}")

    def find_words_by_tag(self, tags: Union[str, List[str]]):
        tags = tags if type(tags) is list else [tags]
        wanted_words = []
        for tag in tags:
            for word in self.words:
                if tag in word.tags:
                    wanted_words.append(word)
        return wanted_words

"""
This module provides a class for text manipulation.

It contains a class Text that provides methods for converting text into normalized form.
"""
from num2words import num2words
import json
import re


class Text:
    """
    A class that provides text manipulation methods.
    """

    def __init__(self, link_replacement: str) -> None:
        self.words = Text.__get_words()
        self._link_pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        self._link_replacement = link_replacement

    def text2norm(self, text: str) -> str:
        """
        Convert a given text into normalized form.

        Parameters:
            text (str): The text to be converted.

        Returns:
            str: The converted text in normalized form.
        """
        result = text.split()
        for i, v in enumerate(result):
            if v.isdigit() and int(v) < 999999999999999999999999999:
                result[i] = num2words(int(v), lang="ru")
                continue
            result[i] = self.__get_fixed_word(v)
        return self.__replace_links(" ".join(result))

    def set_word(self, word: str, fixed_word: str) -> None:
        self.words.update({word: fixed_word})
        with open("words.json", "w", encoding="utf-8") as file:
            json.dump(self.words, file, ensure_ascii=False, indent=4)
    
    def del_word(self, word: str) -> str | None:
        try:
            deleted = self.words.pop(word)
        except KeyError:
            return None
        with open("words.json", "w", encoding="utf-8") as file:
            json.dump(self.words, file, ensure_ascii=False, indent=4)
        return deleted

    def __get_fixed_word(self, word: str) -> str:
        word = word.lower()
        if word in self.words.keys():
            return self.words[word]
        return word

    @staticmethod
    def __get_words() -> dict[str, str]:
        with open("words.json", "r", encoding="utf-8") as file:
            return json.load(file)
    
    def __replace_links(self, string):
        if self._link_replacement:
            return re.sub(self._link_pattern, self._link_replacement, string)
        return re.sub(self._link_pattern, '', string)

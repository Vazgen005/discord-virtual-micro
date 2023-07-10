"""
This module provides a class for text manipulation.

It contains a class Text that provides methods for converting text into normalized form.
"""
from num2words import num2words


class Text:
    """
    A class that provides text manipulation methods.
    """
    @staticmethod
    def text2norm(text: str) -> str:
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
                result[i] = num2words(int(v), lang='ru')
        return ' '.join(result)

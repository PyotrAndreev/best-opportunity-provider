from enum import IntEnum


class FillType(IntEnum):
    NAME = 0
    SURNAME = 1
    FULLNAME = 2
    EMAIL = 3
    PHONE_NUMBER = 4
    CV = 5
    GPA = 6
    DIPLOMA = 7
    RECOMMENDATIONAL_LETTER = 8
    PASSPORT = 9


def match_fill_type(tp: str) -> FillType:
    """
    Maps a string representing a field type to its corresponding FillType enum value.

    Args:
        tp (str): The string representing the field type (e.g., "name", "email").

    Returns:
        FillType: The corresponding FillType enum value, or FillType.NAME if the input string doesn't match any predefined type.
    """

    return {
        "name": FillType.NAME,
        "surname": FillType.SURNAME,
        "fullname": FillType.FULLNAME,
        "email": FillType.EMAIL,
        "telephone": FillType.PHONE_NUMBER,
        "cv_file": FillType.CV,
        "GPA_file": FillType.GPA,
        "diploma_file": FillType.DIPLOMA,
        "recomendation_letter_file": FillType.RECOMMENDATIONAL_LETTER,
        "passport_scan": FillType.PASSPORT
    }.get(tp, FillType.NAME)

from collections import deque
from collections import namedtuple
from functools import wraps


def preprocess_string(function):
    @wraps(function)
    def _preprocess_string(string):
        if not string:
            return []
        return list(function(deque(string)))
    return _preprocess_string


vowels = 'aeiou'
diphthongs = ('ng', 'ts')

type_labels = ('whitespace', 'vowel', 'consonant', 'diphthong')
char_type = namedtuple('CharType', type_labels)(*type_labels)


def get_char_type(char, next_char):
    if char == ' ':
        return char_type.whitespace
    if char in vowels:
        return char_type.vowel
    if next_char is not None and char + next_char in diphthongs:
        return char_type.diphthong
    return char_type.consonant


@preprocess_string
def syllabilise(string):
    syllables = deque()
    while string:
        syllable = deque(string.popleft())
        c_type = get_char_type(syllable[0], string[0] if string else None)
        if c_type == char_type.whitespace:
            while string and string[0] == ' ':
                string.popleft()
        if c_type == char_type.diphthong:
            if string:
                syllable.append(string.popleft())
            c_type = char_type.consonant
        if c_type == char_type.consonant:
            if string and string[0] in vowels:
                syllable.append(string.popleft())
        syllables.append(''.join(syllable))
    return syllables

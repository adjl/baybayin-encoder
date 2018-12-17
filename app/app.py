import functools

from collections import deque
from collections import namedtuple
from functools import wraps


def preprocess_input(_func=None, transform=lambda x: x):
    def _preprocess_input(func):
        @functools.wraps(func)
        def __preprocess_input(inputs):
            if not inputs:
                return []
            return list(func(deque(map(transform, inputs))))
        return __preprocess_input
    if _func is None:
        return _preprocess_input
    return _preprocess_input(_func)


vowels = 'aeiou'
diphthongs = ('ng', 'ts')
modifiers = '\\:'

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


@preprocess_input(transform=str.lower)
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


def parse_syllable(syllable):
    if syllable[-1] == ' ':
        return '', '', ''

    def find_index(i, func):
        while i < len(syllable) and func(syllable[i]):
            i += 1
        return i

    cons_i = find_index(0, lambda char: char not in vowels + modifiers)
    vow_i = find_index(cons_i, lambda char: char in vowels)
    return syllable[:cons_i], syllable[cons_i:vow_i], syllable[vow_i:]

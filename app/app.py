import functools

from collections import defaultdict
from collections import deque
from collections import namedtuple


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
trailing, non_trailing = '/', '='
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


def is_whitespace(syllable):
    consonant, vowel, modifier = parse_syllable(syllable)
    return consonant == vowel == modifier == ''


class SymbolTable(defaultdict):
    def __missing__(self, key):
        self[key] = key
        return key


symbol_table = SymbolTable()
symbol_table.update({'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C'})
symbol_table.update({'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4'})
symbol_table.update({'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8'})


@preprocess_input
def transform(syllables):
    transformed_syllables = deque()
    while syllables:

        if (len(syllables) >= 4 and syllables[0] == syllables[2] and
                syllables[1] == syllables[3]):
            for _ in range(2):
                syllables.popleft()
            syllables.insert(2, '\\')

        if (len(syllables) >= 2 and syllables[0][-1] in vowels and
                syllables[0][0] == syllables[1][0]):
            vwls = ''.join([syllables[i][-1] for i in range(2)])
            syllables.popleft()
            syllables[0] = ''.join([syllables[0], symbol_table[vwls]])

        consonant, vowel, modifier = parse_syllable(syllables.popleft())
        if consonant and not vowel:
            modifier = (trailing
                        if not syllables or is_whitespace(syllables[0])
                        else non_trailing)

        syllable = ''.join([consonant, vowel, modifier])
        transformed_syllables.append(syllable if syllable else ' ')
    return transformed_syllables

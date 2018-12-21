from collections import deque

from app.chars import char_type
from app.chars import get_char_type
from app.chars import modifiers
from app.chars import non_trailing
from app.chars import symbol_table
from app.chars import trailing
from app.chars import vowels
from app.util import preprocess_input


@preprocess_input(transform=str.lower)
def tokenise(string):
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


@preprocess_input
def transform(syllables):
    transformed_syllables = deque()
    while syllables:
        double_words(syllables)
        double_syllables(syllables)
        consonant, vowel, modifier = parse_syllable(syllables.popleft())
        if consonant and not vowel:
            modifier = get_consonant_modifier(syllables)
        syllable = ''.join([consonant, vowel, modifier])
        transformed_syllables.append(syllable if syllable else ' ')
    return transformed_syllables


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


def double_words(syllables):
    if (len(syllables) >= 4 and syllables[0] == syllables[2] and
            syllables[1] == syllables[3]):
        for _ in range(2):
            syllables.popleft()
        syllables.insert(2, '\\')


def double_syllables(syllables):
    if (len(syllables) >= 2 and syllables[0][-1] in vowels and
            syllables[0][0] == syllables[1][0]):
        end_vowels = ''.join([syllables[i][-1] for i in range(2)])
        syllables.popleft()
        syllables[0] = ''.join([syllables[0], symbol_table[end_vowels]])


def get_consonant_modifier(syllables):
    def is_whitespace(syllable):
        consonant, vowel, modifier = parse_syllable(syllable)
        return consonant == vowel == modifier == ''

    if not syllables or is_whitespace(syllables[0]):
        return trailing
    return non_trailing

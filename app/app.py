from collections import deque

from app.char import chartype
from app.char import get_chartype
from app.char import non_trailing
from app.char import symbol_table
from app.char import trailing
from app.util import dequeify_input


@dequeify_input(transform=str.lower)
def tokenise(chars):
    syllables = deque()
    while chars:
        syllable = deque(chars.popleft())
        ctype = get_chartype(syllable[0], chars[0] if chars else None)
        if ctype == 'whitespace':
            while chars and syllable[0] == chars[0]:
                chars.popleft()
        if ctype == 'diphthong':
            syllable.append(chars.popleft())
            ctype = 'consonant'
        if ctype == 'consonant':
            if chars and chars[0] in chartype['vowel']:
                syllable.append(chars.popleft())
        syllables.append(''.join(syllable))
    return syllables


@dequeify_input
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

    cons_i = find_index(0, lambda char: char not in chartype['modified_vowel'])
    vow_i = find_index(cons_i, lambda char: char in chartype['vowel'])
    return syllable[:cons_i], syllable[cons_i:vow_i], syllable[vow_i:]


def double_words(syllables):
    if (len(syllables) >= 4 and syllables[0] == syllables[2] and
            syllables[1] == syllables[3]):
        for _ in range(2):
            syllables.popleft()
        syllables.insert(2, '\\')


def double_syllables(syllables):
    if (len(syllables) >= 2 and syllables[0][-1] in chartype['vowel'] and
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

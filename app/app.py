from collections import deque

from app.char import chars
from app.char import get_char_type
from app.char import parse_syllable
from app.char import symbol_map
from app.util import dequeify_input


@dequeify_input(transform=str.lower)
def tokenise(seq):
    syllables = deque()
    while seq:
        syllable = deque(seq.popleft())
        char_type = get_char_type(syllable[0], seq[0] if seq else None)
        if char_type == 'whitespace':
            while seq and syllable[0] == seq[0]:
                seq.popleft()
        if char_type == 'diphthong':
            syllable.append(seq.popleft())
            char_type = 'consonant'
        if char_type == 'consonant':
            if seq and seq[0] in chars['vowel']:
                syllable.append(seq.popleft())
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


def double_words(syllables):
    if (len(syllables) >= 4 and syllables[0] == syllables[2] and
            syllables[1] == syllables[3]):
        for _ in range(2):
            syllables.popleft()
        syllables.insert(2, '\\')


def double_syllables(syllables):
    if (len(syllables) >= 2 and syllables[0][-1] in chars['vowel'] and
            syllables[0][0] == syllables[1][0]):
        end_vowels = ''.join([syllables[i][-1] for i in range(2)])
        syllables.popleft()
        syllables[0] = ''.join([syllables[0], symbol_map[end_vowels]])


def get_consonant_modifier(syllables):
    def is_whitespace(syllable):
        consonant, vowel, modifier = parse_syllable(syllable)
        return consonant == vowel == modifier == ''
    if not syllables or is_whitespace(syllables[0]):
        return symbol_map['trailing_consonant']
    return symbol_map['non_trailing_consonant']

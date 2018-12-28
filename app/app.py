from collections import deque
from itertools import islice

from app.char import Syllable
from app.char import chars
from app.char import get_char_type
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


@dequeify_input(transform=Syllable)
def transform(syllables):
    transformed = deque()
    while syllables:
        if is_word_doubling(list(islice(syllables, 0, 4))):
            for _ in range(2):
                syllables.popleft()
            syllables.insert(2, Syllable(symbol_map['word_doubling']))
        syllable_slice = list(islice(syllables, 0, 2))
        if (is_vowel_doubling(syllable_slice) or
                is_syllable_doubling(syllable_slice)):
            syllables.popleft()
            syllables[0].modifier = symbol_map[get_vowels(syllable_slice)]
        if is_consonant_stop(list(islice(syllables, 0, 2))):
            syllable = syllables.popleft()
            if syllable.modifier == ':':
                syllable.modifier = ';'
            else:
                syllable.modifier += symbol_map['consonant_stop']
            syllables.popleft()
            syllables.appendleft(syllable)
        if is_trailing_consonant(list(islice(syllables, 0, 2))):
            syllables[0].modifier += symbol_map['trailing_consonant']
        if is_non_trailing_consonant(list(islice(syllables, 0, 2))):
            syllables[0].modifier += symbol_map['non_trailing_consonant']
        transformed.append(syllables.popleft())
    return transformed


def is_word_doubling(syllables):
    if len(syllables) < 4:
        return False
    return ((syllables[0], syllables[1]) == (syllables[2], syllables[3]) and
            syllables[0] != syllables[1])


vowel_repetitions = set(['aa', 'ii', 'ee', 'uu', 'oo', 'ie', 'ei', 'uo', 'ou'])


def is_vowel_doubling(syllables):
    if len(syllables) < 2:
        return False
    return (syllables[0].is_vowel() and syllables[1].is_vowel() and
            syllables[0] == syllables[1])


def is_syllable_doubling(syllables):
    if len(syllables) < 2:
        return False
    return (syllables[0].is_syllable() and syllables[1].is_syllable() and
            syllables[0].consonant == syllables[1].consonant and
            get_vowels(syllables) in vowel_repetitions)


def is_consonant_stop(syllables):
    if len(syllables) < 2:
        return False
    return (syllables[0].is_syllable() and syllables[1].is_consonant() and
            syllables[0].consonant == syllables[1].consonant)


def is_trailing_consonant(syllables):
    if not syllables[0].is_consonant():
        return False
    return len(syllables) < 2 or syllables[1] == Syllable(' ')


def is_non_trailing_consonant(syllables):
    if not syllables[0].is_consonant() or len(syllables) < 2:
        return False
    return syllables[1] != Syllable(' ')


def get_vowels(syllables):
    return ''.join(
        [syllable.vowel for syllable in syllables if syllable.vowel])

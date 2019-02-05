from collections import deque

from app.char import chars
from app.char import get_char_type
from app.char import symbol_map
from app.syllable import Syllable
from app.syllable import SyllableSeq
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
    syllables = SyllableSeq(syllables)
    while syllables:
        if syllables.is_word_doubling():
            for _ in range(2):
                syllables.popleft()
            syllables.insert(2, Syllable(symbol_map['word_doubling']))

        if syllables.is_vowel_doubling() or syllables.is_syllable_doubling():
            syllable_slice = syllables.get_next(2)
            syllables.popleft()
            syllables[0].modifier = symbol_map[get_vowels(syllable_slice)]

        if syllables.is_consonant_stop():
            syllable = syllables.popleft()
            if syllable.modifier == ':':
                syllable.modifier = ';'
            else:
                syllable.modifier += symbol_map['consonant_stop']
            syllables.popleft()
            syllables.appendleft(syllable)

        if syllables.is_trailing_consonant():
            syllables[0].modifier += symbol_map['trailing_consonant']

        if syllables.is_non_trailing_consonant():
            syllables[0].modifier += symbol_map['non_trailing_consonant']

        transformed.append(syllables.popleft())
    return transformed


def get_vowels(syllables):
    return ''.join(
        [syllable.vowel for syllable in syllables if syllable.vowel])

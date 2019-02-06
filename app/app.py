from collections import deque

from app.char import chars
from app.char import get_char_type
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
        if syllables.is_syllable_tripling():
            syllables[1].append_modifier('double_syllable')
            syllables.pop_nth(2)

        if syllables.is_syllable_doubling() or syllables.is_vowel_doubling():
            if syllables[0].is_vowel() and syllables[0].modifier != 'a':
                syllables[0].append_modifier('double_syllable')
            else:
                syllables[0].set_modifier(syllables.concat_vowels(2))
            syllables.pop_nth(1)

        if syllables.is_consonant_stop():
            if syllables[0].is_double_syllable():
                syllables[0].set_modifier('double_syllable_consonant_stop')
            else:
                syllables[0].append_modifier('syllable_consonant_stop')
            syllables.pop_nth(1)

        if syllables.is_trailing_consonant():
            syllables[0].append_modifier('trailing_consonant')

        if syllables.is_non_trailing_consonant():
            syllables[0].append_modifier('non_trailing_consonant')

        transformed.append(syllables.popleft())
    return transformed

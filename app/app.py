from collections import deque

from app.chars import chars
from app.chars import get_char_type
from app.syllable import Syllable
from app.syllable import SyllableSeq
from app.utils import transform_args


@transform_args(transform=str.lower)
def tokenise(string):
    syllables = deque()
    while string:
        syllable = deque(string.popleft())
        char_type = get_char_type(syllable[0], string[0] if string else None)
        if char_type == 'whitespace':
            while string and syllable[0] == string[0]:
                string.popleft()
        if char_type == 'diphthong':
            syllable.append(string.popleft())
            char_type = 'consonant'
        if char_type == 'consonant':
            if string and string[0] in chars['vowel']:
                syllable.append(string.popleft())
        syllables.append(''.join(syllable))
    return syllables


@transform_args(transform=Syllable, seq=SyllableSeq)
def transform(syllables):
    transformed = deque()
    while syllables:
        if syllables[0].is_hyphen():
            syllables.popleft()

        if syllables.is_triple_syllable():
            syllables[1].append_modifier('double_syllable')
            syllables.pop_nth(2)

        if syllables.is_double_syllable():
            if syllables[0].is_vowel() and syllables[0].modifier != 'a':
                syllables[0].append_modifier('double_syllable')
            else:
                syllables[0].set_modifier(syllables.concat_vowels())
            syllables.pop_nth(1)

        if syllables.is_consonant_stop():
            if syllables[0].is_double_syllable():
                syllables[0].set_modifier('double_consonant_stop')
            else:
                syllables[0].append_modifier('consonant_stop')
            syllables.pop_nth(1)

        if syllables.is_trailing_consonant():
            syllables[0].append_modifier('trailing_consonant')

        if syllables.is_non_trailing_consonant():
            syllables[0].append_modifier('non_trailing_consonant')

        transformed.append(syllables.popleft())
    return transformed

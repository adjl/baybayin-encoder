from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_regex

from baybayin_transliterator import symbols
from baybayin_transliterator import transcribe

from .util import num_chars
from .util import strategies


@given(strategies['vowel'])
@settings(max_examples=num_chars['vowel'])
def test_transcribe_vowel(vowel):
    assert transcribe([vowel]) == vowel.upper()


@given(strategies['vowel'])
@settings(max_examples=num_chars['vowel'])
def test_transcribe_vowel_doubled(vowel):
    def concat(*vowels):
        return [''.join([vowel, ':']) for vowel in vowels]
    syllable, expected = concat(vowel, vowel.upper())
    assert transcribe([syllable]) == expected


@given(strategies['consonant'])
@settings(max_examples=num_chars['consonant'])
def test_transcribe_syllable_ends_with_a(consonant):
    syllable = ''.join([consonant, 'a'])
    assert transcribe([syllable]) == symbols[consonant]


@given(strategies['consonant'], from_regex(r'[eiou]', fullmatch=True))
@settings(max_examples=num_chars['consonant'] * 4)
def test_transcribe_syllable(consonant, vowel):
    def concat(*consonants):
        return [''.join([consonant, vowel]) for consonant in consonants]
    syllable, expected = concat(consonant, symbols[consonant])
    assert transcribe([syllable]) == expected


@given(strategies['consonant'], from_regex(r'[-:;]', fullmatch=True))
@settings(max_examples=num_chars['consonant'] * 3)
def test_transcribe_syllable_ends_with_a_with_modifier(consonant, modifier):
    def concat(*syllables):
        syllables = [''.join([*syllable]) for syllable in syllables]
        return [''.join([syllable, modifier]) for syllable in syllables]
    syllable, expected = concat((consonant, 'a'), (symbols[consonant], ''))
    assert transcribe([syllable]) == expected


@given(strategies['consonant'], from_regex(r'[eiou]', fullmatch=True))
@settings(max_examples=num_chars['consonant'] * 4)
def test_transcribe_syllable_with_consonant_stop(consonant, vowel):
    def concat(*consonants):
        return [''.join([consonant, vowel, '-']) for consonant in consonants]
    syllable, expected = concat(consonant, symbols[consonant])
    assert transcribe([syllable]) == expected

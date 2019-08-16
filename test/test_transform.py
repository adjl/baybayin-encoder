from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_regex

from baybayin_transliterator import symbols
from baybayin_transliterator import transform

from .util import num_chars
from .util import strategies


@given(strategies['consonant'])
@settings(max_examples=num_chars['consonant'])
def test_transform_trailing_consonant(consonant):
    expected = ''.join([consonant, symbols['trailing_consonant']])
    assert transform([consonant]) == [expected]


@given(strategies['consonant'], strategies['whitespace'])
@settings(max_examples=num_chars['consonant'] * num_chars['whitespace'])
def test_transform_trailing_consonant_then_whitespace(consonant, whitespace):
    expected = ''.join([consonant, symbols['trailing_consonant']])
    assert transform([consonant, whitespace]) == [expected, whitespace]


@given(strategies['consonant'], strategies['punctuation'])
@settings(max_examples=num_chars['consonant'] * num_chars['punctuation'])
def test_transform_trailing_consonant_then_punctuation(consonant, punctuation):
    expected = ''.join([consonant, symbols['trailing_consonant']])
    assert transform([consonant, punctuation]) == [expected, punctuation]


@given(strategies['consonant'])
@settings(max_examples=num_chars['consonant'])
def test_transform_non_trailing_consonant(consonant):
    expected1 = ''.join([consonant, symbols['non_trailing_consonant']])
    expected2 = ''.join([consonant, symbols['trailing_consonant']])
    assert transform([consonant] * 2) == [expected1, expected2]


@given(strategies['consonant'], strategies['vowel'])
@settings(max_examples=num_chars['consonant'] * num_chars['vowel'])
def test_transform_non_trailing_consonant_then_hyphen(consonant, vowel):
    expected = ''.join([consonant, symbols['non_trailing_consonant']])
    assert transform([consonant, '-', vowel]) == [expected, vowel]


@given(strategies['consonant'], strategies['vowel'])
@settings(max_examples=num_chars['consonant'] * num_chars['vowel'])
def test_transform_consonant_stop(consonant, vowel):
    syllable = ''.join([consonant, vowel])
    expected = ''.join([syllable, symbols['consonant_stop']])
    assert transform([syllable, consonant]) == [expected]


@given(strategies['vowel'])
@settings(max_examples=num_chars['vowel'])
def test_transform_double_vowel(vowel):
    expected = ''.join([vowel, symbols['double_syllable']])
    assert transform([vowel] * 2) == [expected]


@given(strategies['consonant'], strategies['vowel'], strategies['vowel'])
@settings(max_examples=num_chars['consonant'] * 9)
def test_transform_vowel_pattern(consonant, vowel1, vowel2):
    def concat(*vowels):
        return [''.join([consonant, vowel]) for vowel in vowels]
    vowel_pattern = ''.join([vowel1, vowel2])
    assume(vowel_pattern in symbols)
    syllable1, syllable2 = concat(vowel1, vowel2)
    expected = ''.join([syllable1, symbols[vowel_pattern]])
    assert transform([syllable1, syllable2]) == [expected]


@given(strategies['consonant'], strategies['vowel'], strategies['vowel'])
@settings(max_examples=num_chars['consonant'] * 8)
def test_transform_double_syllable_consonant_stop(consonant, vowel1, vowel2):
    def concat(*vowels):
        return [''.join([consonant, vowel]) for vowel in vowels]
    assume(all(vowel in 'eiou' for vowel in [vowel1, vowel2]))
    vowel_pattern = ''.join([vowel1, vowel2])
    assume(vowel_pattern in symbols)
    syllable1, syllable2 = concat(vowel1, vowel2)
    expected = ''.join(
        [syllable1, symbols[vowel_pattern], symbols['consonant_stop']])
    assert transform([syllable1, syllable2, consonant]) == [expected]


@given(strategies['consonant'])
@settings(max_examples=num_chars['consonant'])
def test_transform_double_consonant_stop(consonant):
    syllable = ''.join([consonant, 'a'])
    expected = ''.join([syllable, symbols['double_consonant_stop']])
    assert transform([syllable, syllable, consonant]) == [expected]


@given(from_regex(r'(?:[bdf-hj-npr-tvwyz]|ñ|ng|ts)?[aeiou]', fullmatch=True))
@settings(max_examples=(
    num_chars['consonant'] * num_chars['vowel'] + num_chars['vowel']))
def test_transform_triple_syllable(syllable):
    doubled_syllable = ''.join([syllable, symbols['double_syllable']])
    assert transform([syllable] * 3) == [syllable, doubled_syllable]

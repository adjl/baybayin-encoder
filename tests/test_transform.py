from hypothesis import assume
from hypothesis import given
from hypothesis import settings

from app.app import transform
from app.syllable import Syllable
from app.syllable import vowel_repetitions
from app.symbol import symbols
from tests.util import num_chars
from tests.util import strategies


@given(strategies['consonant'])
@settings(max_examples=num_chars['consonant'])
def test_transform_trailing_consonant(consonant):
    expected = ''.join([consonant, symbols['trailing_consonant']])
    assert transform([consonant]) == [Syllable(expected)]
    assert transform([consonant, ' ']) == [Syllable(expected), Syllable(' ')]


@given(strategies['consonant'])
@settings(max_examples=num_chars['consonant'])
def test_transform_non_trailing_consonant(consonant):
    expected = ''.join([consonant, symbols['non_trailing_consonant']])
    assert transform([consonant] * 2)[0] == Syllable(expected)


@given(strategies['consonant'], strategies['vowel'])
@settings(max_examples=num_chars['consonant'] * num_chars['vowel'])
def test_transform_syllable_consonant_stop(consonant, vowel):
    syllable = ''.join([consonant, vowel])
    expected = ''.join([syllable, symbols['syllable_consonant_stop']])
    assert transform([syllable, consonant]) == [Syllable(expected)]


@given(strategies['consonant'], strategies['vowel'], strategies['vowel'])
@settings(max_examples=num_chars['consonant'] * 9)
def test_transform_vowel_pattern(consonant, vowel1, vowel2):
    vowel_pattern = ''.join([vowel1, vowel2])
    assume(vowel_pattern in vowel_repetitions)
    syllable1 = ''.join([consonant, vowel1])
    syllable2 = ''.join([consonant, vowel2])
    expected = ''.join([syllable1, symbols[vowel_pattern]])
    assert transform([syllable1, syllable2]) == [Syllable(expected)]


def test_transform():
    assert transform(['ba', 'ba', 'b']) == [Syllable('ba;')]
    assert transform(['bi', 'bi', 'b']) == [Syllable('bi1-')]
    assert transform(['be', 'be', 'b']) == [Syllable('be2-')]
    assert transform(['bu', 'bu', 'b']) == [Syllable('bu3-')]
    assert transform(['bo', 'bo', 'b']) == [Syllable('bo4-')]
    assert transform(['bi', 'be', 'b']) == [Syllable('bi5-')]
    assert transform(['be', 'bi', 'b']) == [Syllable('be6-')]
    assert transform(['bu', 'bo', 'b']) == [Syllable('bu7-')]
    assert transform(['bo', 'bu', 'b']) == [Syllable('bo8-')]

    assert transform(['ba', 'ba', 'ba']) == [Syllable('ba'), Syllable('ba:')]

    assert(transform(['bi', 'be', 'bu', 'bo']) ==
           [Syllable('bi5'), Syllable('bu7')])
    assert(transform(['bi', 'bu', 'be', 'bo']) ==
           [Syllable('bi'), Syllable('bu'), Syllable('be'), Syllable('bo')])

    assert transform(['a', 'a']) == [Syllable('a:')]

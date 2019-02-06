from hypothesis import given
from hypothesis import settings

from app.app import transform
from app.syllable import Syllable
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
    assert transform(['ba', 'ba']) == [Syllable('ba:')]
    assert transform(['bi', 'bi']) == [Syllable('bi1')]
    assert transform(['be', 'be']) == [Syllable('be2')]
    assert transform(['bu', 'bu']) == [Syllable('bu3')]
    assert transform(['bo', 'bo']) == [Syllable('bo4')]
    assert transform(['bi', 'be']) == [Syllable('bi5')]
    assert transform(['be', 'bi']) == [Syllable('be6')]
    assert transform(['bu', 'bo']) == [Syllable('bu7')]
    assert transform(['bo', 'bu']) == [Syllable('bo8')]
    assert transform(['ba', 'b']) == [Syllable('ba-')]
    assert transform(['bi', 'b']) == [Syllable('bi-')]
    assert transform(['be', 'b']) == [Syllable('be-')]
    assert transform(['bu', 'b']) == [Syllable('bu-')]
    assert transform(['bo', 'b']) == [Syllable('bo-')]

    assert transform(['ba', 'ba', 'ba']) == [Syllable('ba'), Syllable('ba:')]

    assert(transform(['bi', 'be', 'bu', 'bo']) ==
           [Syllable('bi5'), Syllable('bu7')])
    assert(transform(['bi', 'bu', 'be', 'bo']) ==
           [Syllable('bi'), Syllable('bu'), Syllable('be'), Syllable('bo')])

    assert transform(['a', 'a']) == [Syllable('a:')]

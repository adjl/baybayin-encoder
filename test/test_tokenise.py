import re

from test.utils import num_chars
from test.utils import num_examples
from test.utils import strategies
from test.utils import syllable_re

from hypothesis import assume
from hypothesis import given
from hypothesis import settings

from app.app import tokenise


def test_tokenise_empty_seq():
    assert not tokenise('')


@given(strategies['whitespace'])
@settings(max_examples=num_chars['whitespace'])
def test_tokenise_whitespace(whitespace):
    assert tokenise(whitespace) == [whitespace]


@given(strategies['whitespace'])
@settings(max_examples=num_chars['whitespace'])
def test_tokenise_contiguous_whitespace(whitespace):
    assert tokenise(whitespace * 2) == [whitespace]


@given(strategies['punctuation'])
@settings(max_examples=num_chars['punctuation'])
def test_tokenise_punctuation(punctuation):
    assert tokenise(punctuation) == [punctuation]


@given(strategies['punctuation'], strategies['punctuation'])
@settings(max_examples=num_chars['punctuation'] ** 2)
def test_tokenise_multiple_punctuation(punctuation1, punctuation2):
    punctuation = ''.join([punctuation1, punctuation2])
    assert tokenise(punctuation) == [punctuation1, punctuation2]


@given(strategies['punctuation'], strategies['whitespace'])
@settings(max_examples=num_chars['punctuation'] * num_chars['whitespace'])
def test_tokenise_punctuation_followed_by_whitespace(punctuation, whitespace):
    formatting = ''.join([punctuation, whitespace])
    assert tokenise(formatting) == [punctuation, whitespace]


@given(strategies['syllable'])
@settings(max_examples=num_chars['syllable'])
def test_tokenise_uppercase(lowercase):
    assume(lowercase)
    assert tokenise(lowercase.upper()) == tokenise(lowercase)


@given(strategies['syllable'])
@settings(max_examples=num_chars['syllable'])
def test_tokenise_single_syllable(syllable):
    assume(syllable)
    assert tokenise(syllable) == [syllable]


@given(strategies['syllable'], strategies['syllable'])
@settings(max_examples=num_examples(num_chars['syllable'] ** 2))
def test_tokenise_multiple_syllable_word(syllable1, syllable2):
    assume(syllable1 and syllable2)
    word = ''.join([syllable1, syllable2])
    assume(re.fullmatch(syllable_re, word) is None)
    assert tokenise(word) == [syllable1, syllable2]


@given(strategies['syllable'], strategies['whitespace'],
       strategies['syllable'])
@settings(max_examples=num_examples(
    num_chars['syllable'] ** 2 * num_chars['whitespace']))
def test_tokenise_words(syllable1, whitespace, syllable2):
    assume(syllable1 or syllable2)
    words = ''.join([syllable1, whitespace, syllable2])
    assert(tokenise(words) ==
           [word for word in [syllable1, whitespace, syllable2] if word])


@given(strategies['syllable'], strategies['punctuation'],
       strategies['syllable'])
@settings(max_examples=num_examples(
    num_chars['syllable'] ** 2 * num_chars['punctuation']))
def test_tokenise_words_with_punctuation(syllable1, punctuation, syllable2):
    assume(syllable1 or syllable2)
    words = ''.join([syllable1, punctuation, syllable2])
    assert(tokenise(words) ==
           [word for word in [syllable1, punctuation, syllable2] if word])


@given(strategies['syllable'], strategies['punctuation'],
       strategies['whitespace'], strategies['syllable'])
@settings(max_examples=num_examples(
    num_chars['syllable'] ** 2 * num_chars['punctuation'] *
    num_chars['whitespace']))
def test_tokenise_phrase_with_punctuation(
        syllable1, punctuation, whitespace, syllable2):
    assume(syllable1 or syllable2)
    phrase = ''.join([syllable1, punctuation, whitespace, syllable2])
    assert(tokenise(phrase) ==
           [word for word in
            [syllable1, punctuation, whitespace, syllable2] if word])

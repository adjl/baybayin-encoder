import re

from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_regex

from app.app import tokenise


syllable_pattern = re.compile(r'([bdf-hj-npr-tvwyz]|ñ|ng|ts)?[aeiou]?')
syllable_strategy = from_regex(syllable_pattern, fullmatch=True)
num_syllables = 131  # 21 consonants * 5 vowels + 21 + 5


def num_examples(num):
    # return num  # Uncomment to generate all test data. Warning: slow! (~50s)
    return min(settings.default.max_examples, num)


def test_tokenise_empty_string():
    assert tokenise('') == []


@given(from_regex(r'(?a)\s', fullmatch=True))
@settings(max_examples=6)  # \s regex: len([ \t\n\r\f\v]) = 6
def test_tokenise_whitespace(whitespace):
    assert tokenise(whitespace) == [whitespace]


@given(from_regex(r'(?a)\s', fullmatch=True))
@settings(max_examples=6)  # \s regex: len([ \t\n\r\f\v]) = 6
def test_tokenise_contiguous_whitespace(whitespace):
    assert tokenise(whitespace * 2) == [whitespace]


@given(syllable_strategy)
@settings(max_examples=num_examples(num_syllables))
def test_tokenise_uppercase(lowercase):
    assume(lowercase)
    assert tokenise(lowercase.upper()) == tokenise(lowercase)


@given(syllable_strategy)
@settings(max_examples=num_examples(num_syllables))
def test_tokenise_single_syllable(syllable):
    assume(syllable)
    assert tokenise(syllable) == [syllable]


@given(syllable_strategy, syllable_strategy)
@settings(max_examples=num_examples(num_syllables * num_syllables))
def test_tokenise_multiple_syllables(syllable1, syllable2):
    assume(syllable1 and syllable2)
    syllables = ''.join([syllable1, syllable2])
    assume(re.fullmatch(syllable_pattern, syllables) is None)
    assert tokenise(syllables) == [syllable1, syllable2]


@given(syllable_strategy, syllable_strategy)
@settings(max_examples=num_examples(num_syllables * num_syllables))
def test_tokenise_words(syllable1, syllable2):
    words = ''.join([syllable1, ' ', syllable2])
    assert(tokenise(words) ==
           [word for word in [syllable1, ' ', syllable2] if word])
    words = ''.join([syllable2, ' ', syllable1])
    assert(tokenise(words) ==
           [word for word in [syllable2, ' ', syllable1] if word])

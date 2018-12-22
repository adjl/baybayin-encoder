import re

from hypothesis import assume
from hypothesis import given
from hypothesis import settings
from hypothesis.strategies import from_regex

from app.app import tokenise


diphthong_pattern = re.compile(r'ng|ts')
syllable_pattern = re.compile(r'([bdf-hj-npr-tvwyz]|ñ|ng|ts)[aeiou]')


whitespace_strategy = from_regex(r'(?a)\s', fullmatch=True)
uppercase_strategy = from_regex(
    r'[AEIOU]|([BDF-HJ-NPR-TVWYZ]|Ñ|NG|TS)[AEIOU]?',
    fullmatch=True)

vowel_strategy = from_regex(r'[aeiou]', fullmatch=True)
consonant_strategy = from_regex(r'[bdf-hj-npr-tvwyz]|ñ|ng|ts',
                                fullmatch=True)
syllable_strategy = from_regex(r'([bdf-hj-npr-tvwyz]|ñ|ng|ts)[aeiou]',
                               fullmatch=True)


num_whitespace = 6
num_vowels = 5
num_consonants = 21
num_syllables = num_consonants * num_vowels
num_single_syllables = num_consonants * (num_vowels + 1) + num_vowels

derandomised = settings(derandomize=True)


def num_examples(num):
    return min(settings.default.max_examples, num)


def test_tokenise_empty_string():
    assert tokenise('') == []


@given(whitespace_strategy)
@settings(derandomised, max_examples=num_examples(num_whitespace))
def test_tokenise_whitespace(whitespace):
    assert tokenise(whitespace) == [whitespace]


@given(whitespace_strategy)
@settings(derandomised, max_examples=num_examples(num_whitespace))
def test_tokenise_contiguous_whitespace(whitespace):
    assert tokenise(whitespace * 2) == [whitespace]


@given(uppercase_strategy)
@settings(derandomised, max_examples=num_examples(num_single_syllables))
def test_tokenise_lowercase(uppercase):
    assert all([char.islower() for char in tokenise(uppercase)])


@given(vowel_strategy)
@settings(derandomised, max_examples=num_examples(num_vowels))
def test_tokenise_single_syllable_vowel(vowel):
    assert tokenise(vowel) == [vowel]


@given(consonant_strategy)
@settings(derandomised, max_examples=num_examples(num_consonants))
def test_tokenise_single_syllable_consonant(consonant):
    assert tokenise(consonant) == [consonant]


@given(syllable_strategy)
@settings(derandomised, max_examples=num_examples(num_syllables))
def test_tokenise_single_syllable(syllable):
    assert tokenise(syllable) == [syllable]


@given(vowel_strategy, vowel_strategy)
@settings(derandomised, max_examples=num_examples(num_vowels * num_vowels))
def test_tokenise_multiple_syllables_vowels(vowel1, vowel2):
    syllables = ''.join([vowel1, vowel2])
    assert tokenise(syllables) == [vowel1, vowel2]


@given(consonant_strategy, consonant_strategy)
@settings(derandomised,
          max_examples=num_examples(num_consonants * num_consonants))
def test_tokenise_multiple_syllables_consonants(consonant1, consonant2):
    syllables = ''.join([consonant1, consonant2])
    assume(re.fullmatch(diphthong_pattern, syllables) is None)
    assert tokenise(syllables) == [consonant1, consonant2]


@given(vowel_strategy, consonant_strategy)
@settings(derandomised, max_examples=num_examples(num_vowels * num_consonants))
def test_tokenise_multiple_syllables_vowel_consonant(vowel, consonant):
    syllables = ''.join([vowel, consonant])
    assert tokenise(syllables) == [vowel, consonant]


@given(vowel_strategy, syllable_strategy)
@settings(derandomised, max_examples=num_examples(num_vowels * num_syllables))
def test_tokenise_multiple_syllables_vowel_syllable(vowel, syllable):
    syllables = ''.join([vowel, syllable])
    assert tokenise(syllables) == [vowel, syllable]
    syllables = ''.join([syllable, vowel])
    assert tokenise(syllables) == [syllable, vowel]


@given(consonant_strategy, syllable_strategy)
@settings(derandomised,
          max_examples=num_examples(num_consonants * num_syllables))
def test_tokenise_multiple_syllables_consonants_syllable(consonant, syllable):
    syllables = ''.join([consonant, syllable])
    assume(re.fullmatch(syllable_pattern, syllables) is None)
    assert tokenise(syllables) == [consonant, syllable]
    syllables = ''.join([syllable, consonant])
    assert tokenise(syllables) == [syllable, consonant]


@given(syllable_strategy, syllable_strategy)
@settings(derandomised,
          max_examples=num_examples(num_syllables * num_syllables))
def test_tokenise_multiple_syllables(syllable1, syllable2):
    syllables = ''.join([syllable1, syllable2])
    assert tokenise(syllables) == [syllable1, syllable2]


def test_tokenise_words():
    assert tokenise(' a') == [' ', 'a']
    assert tokenise('a ') == ['a', ' ']
    assert tokenise('b a') == ['b', ' ', 'a']
    assert tokenise('ba ba') == ['ba', ' ', 'ba']


def test_tokenise_words_diphthong_ng():
    assert tokenise(' ng') == [' ', 'ng']
    assert tokenise('ng ') == ['ng', ' ']
    assert tokenise('ng n') == ['ng', ' ', 'n']
    assert tokenise('ng ng') == ['ng', ' ', 'ng']
    assert tokenise('n gn') == ['n', ' ', 'g', 'n']
    assert tokenise('ngn g') == ['ng', 'n', ' ', 'g']


def test_tokenise_words_diphthong_ts():
    assert tokenise(' ts') == [' ', 'ts']
    assert tokenise('ts ') == ['ts', ' ']
    assert tokenise('ts t') == ['ts', ' ', 't']
    assert tokenise('ts ts') == ['ts', ' ', 'ts']
    assert tokenise('t st') == ['t', ' ', 's', 't']
    assert tokenise('tst s') == ['ts', 't', ' ', 's']

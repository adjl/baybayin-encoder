import re

from hypothesis import settings
from hypothesis.strategies import from_regex


syllable_re = re.compile(r'(?:[bdf-hj-npr-tvwyz]|ñ|ng|ts)?[aeiou]?')

strategies = {
    'whitespace': from_regex(r'(?a)\s', fullmatch=True),
    'punctuation': from_regex(r'[,.?!<>()]', fullmatch=True),
    'vowel': from_regex(r'[aeiou]', fullmatch=True),
    'consonant': from_regex(r'[bdf-hj-npr-tvwyz]|ñ|ng|ts', fullmatch=True),
    'syllable': from_regex(syllable_re, fullmatch=True)
}

num_chars = {
    'whitespace': 6,  # \s regex: len([ \t\n\r\f\v]) == 6
    'punctuation': 8,
    'vowel': 5,
    'consonant': 21,
    'syllable': 131  # 21 consonants * 5 vowels + 21 + 5
}


def num_examples(num):
    # return num  # Uncomment to generate all test data. Warning: slow! (~50s)
    return min(settings.default.max_examples * 2, num)

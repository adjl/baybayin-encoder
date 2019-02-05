import string

from collections import defaultdict


chars = {
    'whitespace': string.whitespace,
    'punctuation': string.punctuation,
    'digits': string.digits,
    'vowel': 'aeiou',
    'diphthong': ['ng', 'ts']}

chars['non-consonant'] = ''.join(
    [chars[char_type] for char_type in ['whitespace', 'punctuation', 'digits', 'vowel']])


def get_char_type(char, next_char):
    for char_type in ['whitespace', 'punctuation', 'vowel']:
        if char in chars[char_type]:
            return char_type
    if concat(char, next_char) in chars['diphthong']:
        return 'diphthong'
    return 'consonant'


def concat(char, next_char):
    if next_char is None:
        return char
    return ''.join([char, next_char])


class SymbolMap(defaultdict):
    def __missing__(self, key):
        self[key] = key
        return key


symbol_map = SymbolMap()
symbol_map.update({'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C'})
symbol_map.update({'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4'})
symbol_map.update({'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8'})
symbol_map.update({'trailing_consonant': '/', 'non_trailing_consonant': '='})
symbol_map.update({'word_doubling': '\\', 'consonant_stop': '-'})

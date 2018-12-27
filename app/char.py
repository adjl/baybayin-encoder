import string

from collections import defaultdict


class SymbolMap(defaultdict):
    def __missing__(self, key):
        self[key] = key
        return key


def parse_syllable(syllable):
    def get_index(i, func):
        while i < len(syllable) and func(syllable[i]):
            i += 1
        return i
    cons_i = get_index(0, lambda char: char not in chars['non-consonant'])
    vowl_i = get_index(cons_i, lambda char: char in chars['vowel'])
    return syllable[:cons_i], syllable[cons_i:vowl_i], syllable[vowl_i:]


def concat(char, next_char):
    if next_char is None:
        return char
    return ''.join([char, next_char])


def get_char_type(char, next_char):
    for name in ['whitespace', 'punctuation', 'vowel']:
        if char in chars[name]:
            return name
    if concat(char, next_char) in chars['diphthong']:
        return 'diphthong'
    return 'consonant'


symbol_map = SymbolMap()
symbol_map.update({'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C'})
symbol_map.update({'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4'})
symbol_map.update({'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8'})
symbol_map.update({'trailing_consonant': '/', 'non_trailing_consonant': '='})


chars = {
    'whitespace': string.whitespace,
    'punctuation': string.punctuation,
    'vowel': 'aeiou',
    'diphthong': ['ng', 'ts']}
chars['non-consonant'] = ''.join(
    [chars[name] for name in ['whitespace', 'punctuation', 'vowel']])

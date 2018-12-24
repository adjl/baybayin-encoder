import string

from collections import defaultdict


class SymbolMap(defaultdict):
    def __missing__(self, key):
        self[key] = key
        return key


symbol_map = SymbolMap()
symbol_map.update({'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C'})
symbol_map.update({'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4'})
symbol_map.update({'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8'})
symbol_map.update({'trailing_consonant': '/', 'non_trailing_consonant': '='})


chars = {
    'whitespace': string.whitespace,
    'vowel': 'aeiou',
    'diphthong': ['ng', 'ts'],
    'modifier': '\\:'}
chars['vowel+modifier'] = ''.join([chars['vowel'], chars['modifier']])


def concat(char, next_char):
    if next_char is None:
        return char
    return ''.join([char, next_char])


def get_char_type(char, next_char):
    for name in ['whitespace', 'vowel']:
        if char in chars[name]:
            return name
    if concat(char, next_char) in chars['diphthong']:
        return 'diphthong'
    return 'consonant'

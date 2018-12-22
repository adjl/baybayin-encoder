import string

from collections import defaultdict


class SymbolTable(defaultdict):
    def __missing__(self, key):
        self[key] = key
        return key


symbol_table = SymbolTable()
symbol_table.update({'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C'})
symbol_table.update({'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4'})
symbol_table.update({'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8'})


trailing, non_trailing = '/', '='

chartype = {
    'whitespace': string.whitespace,
    'vowel': 'aeiou',
    'diphthong': ['ng', 'ts'],
    'modifier': '\\:'}
chartype['modified_vowel'] = ''.join([chartype['vowel'], chartype['modifier']])


def concat(char, next_char):
    if next_char is None:
        return char
    return ''.join([char, next_char])


def get_chartype(char, next_char):
    for name in ['whitespace', 'vowel']:
        if char in chartype[name]:
            return name
    if concat(char, next_char) in chartype['diphthong']:
        return 'diphthong'
    return 'consonant'

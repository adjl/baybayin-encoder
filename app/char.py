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


def parse_syllable(syllable):
    def get_index(i, func):
        while i < len(syllable) and func(syllable[i]):
            i += 1
        return i
    cons_i = get_index(0, lambda char: char not in chars['non-consonant'])
    vowl_i = get_index(cons_i, lambda char: char in chars['vowel'])
    return syllable[:cons_i], syllable[cons_i:vowl_i], syllable[vowl_i:]


class Syllable:

    def __init__(self, syllable):
        consonant, vowel, modifier = parse_syllable(syllable)
        self._consonant = consonant
        self._vowel = vowel
        self._modifier = modifier

    def __repr__(self):
        return '({},{},{})'.format(self.consonant, self.vowel, self.modifier)

    def __eq__(self, syllable):
        return (self.consonant == syllable.consonant and
                self.vowel == syllable.vowel and
                self.modifier == syllable.modifier)

    def is_consonant(self):
        return self.consonant and not self.vowel

    def is_vowel(self):
        return not self.consonant and self.vowel

    def is_syllable(self):
        return self.consonant and self.vowel

    @property
    def consonant(self):
        return self._consonant

    @property
    def vowel(self):
        return self._vowel

    @property
    def modifier(self):
        return self._modifier

    @vowel.setter
    def vowel(self, vowel):
        self._vowel = vowel

    @modifier.setter
    def modifier(self, modifier):
        self._modifier = modifier


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

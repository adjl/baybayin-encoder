from collections import defaultdict
from collections import namedtuple


class SymbolTable(defaultdict):
    def __missing__(self, key):
        self[key] = key
        return key


symbol_table = SymbolTable()
symbol_table.update({'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C'})
symbol_table.update({'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4'})
symbol_table.update({'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8'})


vowels = 'aeiou'
diphthongs = ('ng', 'ts')
modifiers = '\\:'
trailing, non_trailing = '/', '='

type_labels = ('whitespace', 'vowel', 'consonant', 'diphthong')
char_type = namedtuple('CharType', type_labels)(*type_labels)


def get_char_type(char, next_char):
    if char == ' ':
        return char_type.whitespace
    if char in vowels:
        return char_type.vowel
    if next_char is not None and char + next_char in diphthongs:
        return char_type.diphthong
    return char_type.consonant

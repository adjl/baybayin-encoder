from collections import defaultdict


class SymbolMap(defaultdict):

    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)

    def __missing__(self, key):
        self[key] = key
        return key


symbols = SymbolMap({
    'j': 'D', 'ñ': '~', 'ng': 'N', 'ts': 'C',
    'aa': ':', 'ii': '1', 'ee': '2', 'uu': '3', 'oo': '4',
    'ie': '5', 'ei': '6', 'uo': '7', 'ou': '8',
    'trailing_consonant': '/',
    'non_trailing_consonant': '=',
    'double_syllable': ':',
    'syllable_consonant_stop': '-',
    'double_syllable_consonant_stop': ';'})

import string


chars = {
    'whitespace': string.whitespace,
    'punctuation': string.punctuation,
    'digit': string.digits,
    'vowel': 'aeiou',
    'diphthong': ('ng', 'ts')
}

chars['non-consonant'] = ''.join(
    (chars[char_type] for char_type in ('whitespace', 'punctuation', 'digit', 'vowel')))


def get_char_type(char, next_char):
    for char_type in ('whitespace', 'punctuation', 'vowel'):
        if char in chars[char_type]:
            return char_type
    if concat(char, next_char) in chars['diphthong']:
        return 'diphthong'
    return 'consonant'


def concat(char, next_char):
    if next_char is None:
        return char
    return ''.join((char, next_char))

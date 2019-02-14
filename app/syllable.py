from app.chars import chars
from app.symbols import symbols


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
        self._fields = None

    def __repr__(self):
        if self._fields is None:
            self._set_fields()
        return '({},{},{})'.format(*self._fields)

    def __str__(self):
        if self._fields is None:
            self._set_fields()
        return ''.join(self._fields)

    def __eq__(self, syllable):
        if isinstance(syllable, Syllable):
            return (self.consonant == syllable.consonant and
                    self.vowel == syllable.vowel and
                    self.modifier == syllable.modifier)
        return str(self) == syllable

    def _set_fields(self):
        self._fields = [self.consonant, self.vowel, self.modifier]

    def set_modifier(self, modifier_key):
        self.modifier = symbols[modifier_key]

    def append_modifier(self, modifier_key):
        self.modifier += symbols[modifier_key]

    def is_syllable(self):
        return self.is_vowel() or self.consonant and self.vowel

    def is_consonant(self):
        return self.consonant and not self.vowel

    def is_vowel(self):
        return not self.consonant and self.vowel

    def is_modifier(self):
        return not self.consonant and not self.vowel

    def has_modifier(self):
        return self.modifier

    def is_double_syllable(self):
        return self.modifier == symbols['double_syllable']

    def is_hyphen(self):
        return self.is_modifier() and self.modifier == '-'

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

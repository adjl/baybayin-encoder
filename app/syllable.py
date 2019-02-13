from collections import deque
from itertools import islice

from app.chars import chars
from app.symbols import symbols


vowel_patterns = set([
    'aa', 'ii', 'ee', 'uu', 'oo',
    'ie', 'ei', 'uo', 'ou'])


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
        return self.is_modifier() and self.modifier == symbols['hyphen']

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


class SyllableSeq(deque):

    def __init__(self, syllables):
        super().__init__(syllables)

    def __eq__(self, syllables):
        return [str(syllable) for syllable in self] == syllables

    def concat_vowels(self):
        return ''.join([syllable.vowel for syllable in
                        islice(self, 0, 2) if syllable.vowel])

    def are_all(self, func, n):
        return all(func(syllable) for syllable in islice(self, 0, n))

    def is_triple_syllable(self):
        if len(self) < 3:
            return False
        return (self.are_all(Syllable.is_syllable, 3) and
                self.are_all(lambda s: not s.has_modifier(), 3) and
                self[0] == self[1] == self[2])

    def is_double_syllable(self):
        if len(self) < 2:
            return False
        return (self.are_all(Syllable.is_syllable, 2) and
                self.are_all(lambda s: not s.has_modifier(), 2) and
                self.concat_vowels() in vowel_patterns and
                self[0].consonant == self[1].consonant)

    def is_consonant_stop(self):
        if len(self) < 2:
            return False
        return (self[0].is_syllable() and self[1].is_consonant() and
                self[0].consonant == self[1].consonant)

    def is_trailing_consonant(self):
        if not self[0].is_consonant():
            return False
        return len(self) < 2 or self[1] == Syllable(' ')

    def is_non_trailing_consonant(self):
        if not self[0].is_consonant() or len(self) < 2:
            return False
        return self[1] != Syllable(' ')

    def pop_nth(self, n):
        self.rotate(-n)
        self.popleft()
        self.rotate(n)

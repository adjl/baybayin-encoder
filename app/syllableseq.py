from collections import deque
from itertools import islice

from app.syllable import Syllable
from app.syllable import vowel_patterns


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

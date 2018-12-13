from collections import deque
from collections import namedtuple


whitespace = ' '
vowels = 'aeiou'
diphthongs = ('ng', 'ts')
state_names = ('whitespace', 'vowel', 'consonant', 'diphthong')
states = namedtuple('State', state_names)(*state_names)


def get_state(char, next_char):
    if char == whitespace:
        return states.whitespace
    if char in vowels:
        return states.vowel
    if next_char is not None and char + next_char in diphthongs:
        return states.diphthong
    return states.consonant


def preprocess_input(function):
    def _preprocess_input(string):
        if not string:
            return []
        return list(function(deque(string)))
    return _preprocess_input


@preprocess_input
def syllabilise(string):
    syllables = deque()
    while string:
        syllable = deque(string.popleft())
        state = get_state(syllable[0], string[0] if string else None)
        if state == states.whitespace:
            while string and string[0] == whitespace:
                string.popleft()
        if state == states.diphthong:
            if string:
                syllable.append(string.popleft())
            state = states.consonant
        if state == states.consonant:
            if string and string[0] in vowels:
                syllable.append(string.popleft())
        syllables.append(''.join(syllable))
    return syllables

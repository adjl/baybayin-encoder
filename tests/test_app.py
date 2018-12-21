from app.app import parse_syllable
from app.app import transform


def test_transform():
    assert transform(['b']) == ['b/']
    assert transform(['b', ' ']) == ['b/', ' ']
    assert transform(['b', 'b']) == ['b=', 'b/']


def test_transform_word_doubling():
    assert transform(['ba', 'ka'] * 2) == ['ba', 'ka', '\\']


def test_transform_syllable_doubling():
    assert transform(['a', 'a']) == ['a:']
    assert transform(['ba', 'ba']) == ['ba:']
    assert transform(['bi', 'bi']) == ['bi1']
    assert transform(['bi', 'be']) == ['be5']


def test_parse_syllable():
    assert parse_syllable(' ') == ('', '', '')
    assert parse_syllable('a') == ('', 'a', '')
    assert parse_syllable('b') == ('b', '', '')
    assert parse_syllable('ba') == ('b', 'a', '')


def test_parse_syllable_diphthong():
    assert parse_syllable('ng') == ('ng', '', '')
    assert parse_syllable('ts') == ('ts', '', '')
    assert parse_syllable('nga') == ('ng', 'a', '')
    assert parse_syllable('tsa') == ('ts', 'a', '')


def test_parse_syllable_modifier():
    assert parse_syllable('\\') == ('', '', '\\')
    assert parse_syllable('a:') == ('', 'a', ':')
    assert parse_syllable('b:') == ('b', '', ':')
    assert parse_syllable('ba:') == ('b', 'a', ':')


def test_parse_syllable_diphthong_modifier():
    assert parse_syllable('ng:') == ('ng', '', ':')
    assert parse_syllable('ts:') == ('ts', '', ':')
    assert parse_syllable('nga:') == ('ng', 'a', ':')
    assert parse_syllable('tsa:') == ('ts', 'a', ':')

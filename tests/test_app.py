from app.app import parse_syllable


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

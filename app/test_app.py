from app import syllabilise


def test_syllabilise_empty_string():
    assert syllabilise('') == []


def test_syllabilise_lowercase():
    assert syllabilise('A') == ['a']


def test_syllabilise_single_syllable():
    assert syllabilise('a') == ['a']
    assert syllabilise('b') == ['b']
    assert syllabilise('ba') == ['ba']


def test_syllabilise_single_syllable_diphthongs():
    assert syllabilise('ng') == ['ng']
    assert syllabilise('ts') == ['ts']
    assert syllabilise('nga') == ['nga']
    assert syllabilise('tsa') == ['tsa']


def test_syllabilise_multiple_syllables():
    assert syllabilise('aa') == ['a', 'a']
    assert syllabilise('ab') == ['a', 'b']
    assert syllabilise('bb') == ['b', 'b']
    assert syllabilise('aba') == ['a', 'ba']
    assert syllabilise('baa') == ['ba', 'a']
    assert syllabilise('bab') == ['ba', 'b']
    assert syllabilise('bba') == ['b', 'ba']
    assert syllabilise('baba') == ['ba', 'ba']


def test_syllabilise_multiple_syllables_diphthong_ng():
    assert syllabilise('gn') == ['g', 'n']
    assert syllabilise('ang') == ['a', 'ng']
    assert syllabilise('bng') == ['b', 'ng']
    assert syllabilise('ngb') == ['ng', 'b']
    assert syllabilise('bang') == ['ba', 'ng']
    assert syllabilise('ngab') == ['nga', 'b']
    assert syllabilise('ngng') == ['ng', 'ng']


def test_syllabilise_multiple_syllables_diphthong_ts():
    assert syllabilise('st') == ['s', 't']
    assert syllabilise('ats') == ['a', 'ts']
    assert syllabilise('bts') == ['b', 'ts']
    assert syllabilise('tsb') == ['ts', 'b']
    assert syllabilise('bats') == ['ba', 'ts']
    assert syllabilise('tsab') == ['tsa', 'b']
    assert syllabilise('tsts') == ['ts', 'ts']


def test_syllabilise_whitespace():
    assert syllabilise(' ') == [' ']
    assert syllabilise('  ') == [' ']
    assert syllabilise(' a') == [' ', 'a']
    assert syllabilise('a ') == ['a', ' ']
    assert syllabilise('b a') == ['b', ' ', 'a']
    assert syllabilise('ba ba') == ['ba', ' ', 'ba']


def test_syllabilise_whitespace_diphthong_ng():
    assert syllabilise(' ng') == [' ', 'ng']
    assert syllabilise('ng ') == ['ng', ' ']
    assert syllabilise('ng n') == ['ng', ' ', 'n']
    assert syllabilise('ng ng') == ['ng', ' ', 'ng']
    assert syllabilise('n gn') == ['n', ' ', 'g', 'n']
    assert syllabilise('ngn g') == ['ng', 'n', ' ', 'g']


def test_syllabilise_whitespace_diphthong_ts():
    assert syllabilise(' ts') == [' ', 'ts']
    assert syllabilise('ts ') == ['ts', ' ']
    assert syllabilise('ts t') == ['ts', ' ', 't']
    assert syllabilise('ts ts') == ['ts', ' ', 'ts']
    assert syllabilise('t st') == ['t', ' ', 's', 't']
    assert syllabilise('tst s') == ['ts', 't', ' ', 's']

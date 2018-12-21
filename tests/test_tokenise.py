from app.app import tokenise


def test_tokenise_empty_string():
    assert tokenise('') == []


def test_tokenise_lowercase():
    assert tokenise('A') == ['a']


def test_tokenise_single_syllable():
    assert tokenise('a') == ['a']
    assert tokenise('b') == ['b']
    assert tokenise('ba') == ['ba']


def test_tokenise_single_syllable_diphthong():
    assert tokenise('ng') == ['ng']
    assert tokenise('ts') == ['ts']
    assert tokenise('nga') == ['nga']
    assert tokenise('tsa') == ['tsa']


def test_tokenise_multiple_syllables():
    assert tokenise('aa') == ['a', 'a']
    assert tokenise('ab') == ['a', 'b']
    assert tokenise('bb') == ['b', 'b']
    assert tokenise('aba') == ['a', 'ba']
    assert tokenise('baa') == ['ba', 'a']
    assert tokenise('bab') == ['ba', 'b']
    assert tokenise('bba') == ['b', 'ba']
    assert tokenise('baba') == ['ba', 'ba']


def test_tokenise_multiple_syllables_diphthong_ng():
    assert tokenise('gn') == ['g', 'n']
    assert tokenise('ang') == ['a', 'ng']
    assert tokenise('bng') == ['b', 'ng']
    assert tokenise('ngb') == ['ng', 'b']
    assert tokenise('bang') == ['ba', 'ng']
    assert tokenise('ngab') == ['nga', 'b']
    assert tokenise('ngng') == ['ng', 'ng']


def test_tokenise_multiple_syllables_diphthong_ts():
    assert tokenise('st') == ['s', 't']
    assert tokenise('ats') == ['a', 'ts']
    assert tokenise('bts') == ['b', 'ts']
    assert tokenise('tsb') == ['ts', 'b']
    assert tokenise('bats') == ['ba', 'ts']
    assert tokenise('tsab') == ['tsa', 'b']
    assert tokenise('tsts') == ['ts', 'ts']


def test_tokenise_whitespace():
    assert tokenise(' ') == [' ']
    assert tokenise('  ') == [' ']
    assert tokenise(' a') == [' ', 'a']
    assert tokenise('a ') == ['a', ' ']
    assert tokenise('b a') == ['b', ' ', 'a']
    assert tokenise('ba ba') == ['ba', ' ', 'ba']


def test_tokenise_whitespace_diphthong_ng():
    assert tokenise(' ng') == [' ', 'ng']
    assert tokenise('ng ') == ['ng', ' ']
    assert tokenise('ng n') == ['ng', ' ', 'n']
    assert tokenise('ng ng') == ['ng', ' ', 'ng']
    assert tokenise('n gn') == ['n', ' ', 'g', 'n']
    assert tokenise('ngn g') == ['ng', 'n', ' ', 'g']


def test_tokenise_whitespace_diphthong_ts():
    assert tokenise(' ts') == [' ', 'ts']
    assert tokenise('ts ') == ['ts', ' ']
    assert tokenise('ts t') == ['ts', ' ', 't']
    assert tokenise('ts ts') == ['ts', ' ', 'ts']
    assert tokenise('t st') == ['t', ' ', 's', 't']
    assert tokenise('tst s') == ['ts', 't', ' ', 's']

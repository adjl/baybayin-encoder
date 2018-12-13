from app import syllabilise


def test_syllabilise_empty_string():
    assert syllabilise('') == []


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
    assert syllabilise('ang') == ['a', 'ng']
    assert syllabilise('bng') == ['b', 'ng']
    assert syllabilise('ngb') == ['ng', 'b']
    assert syllabilise('bang') == ['ba', 'ng']
    assert syllabilise('ngab') == ['nga', 'b']
    assert syllabilise('ngng') == ['ng', 'ng']


def test_syllabilise_multiple_syllables_diphthong_ts():
    assert syllabilise('ats') == ['a', 'ts']
    assert syllabilise('bts') == ['b', 'ts']
    assert syllabilise('tsb') == ['ts', 'b']
    assert syllabilise('bats') == ['ba', 'ts']
    assert syllabilise('tsab') == ['tsa', 'b']
    assert syllabilise('tsts') == ['ts', 'ts']

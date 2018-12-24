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

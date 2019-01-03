from app.app import transform
from app.char import Syllable


def test_transform():
    assert(transform(['ba', 'ka', 'ba', 'ka']) ==
           [Syllable('ba'), Syllable('ka'), Syllable('\\')])
    assert transform(['ba', 'ba', 'b']) == [Syllable('ba;')]
    assert transform(['bi', 'bi', 'b']) == [Syllable('bi1-')]
    assert transform(['be', 'be', 'b']) == [Syllable('be2-')]
    assert transform(['bu', 'bu', 'b']) == [Syllable('bu3-')]
    assert transform(['bo', 'bo', 'b']) == [Syllable('bo4-')]
    assert transform(['bi', 'be', 'b']) == [Syllable('be5-')]
    assert transform(['be', 'bi', 'b']) == [Syllable('bi6-')]
    assert transform(['bu', 'bo', 'b']) == [Syllable('bo7-')]
    assert transform(['bo', 'bu', 'b']) == [Syllable('bu8-')]
    assert transform(['ba', 'ba']) == [Syllable('ba:')]
    assert transform(['bi', 'bi']) == [Syllable('bi1')]
    assert transform(['be', 'be']) == [Syllable('be2')]
    assert transform(['bu', 'bu']) == [Syllable('bu3')]
    assert transform(['bo', 'bo']) == [Syllable('bo4')]
    assert transform(['bi', 'be']) == [Syllable('be5')]
    assert transform(['be', 'bi']) == [Syllable('bi6')]
    assert transform(['bu', 'bo']) == [Syllable('bo7')]
    assert transform(['bo', 'bu']) == [Syllable('bu8')]
    assert transform(['ba', 'b']) == [Syllable('ba-')]
    assert transform(['bi', 'b']) == [Syllable('bi-')]
    assert transform(['be', 'b']) == [Syllable('be-')]
    assert transform(['bu', 'b']) == [Syllable('bu-')]
    assert transform(['bo', 'b']) == [Syllable('bo-')]

    assert(transform(['ba', 'ba', 'ba', 'ba']) ==
           [Syllable('ba:'), Syllable('ba:')])
    assert(transform(['bi', 'be', 'bu', 'bo']) ==
           [Syllable('be5'), Syllable('bo7')])
    assert(transform(['bi', 'bu', 'be', 'bo']) ==
           [Syllable('bi'), Syllable('bu'), Syllable('be'), Syllable('bo')])

    assert transform(['a', 'a']) == [Syllable('a:')]

    assert transform(['b']) == [Syllable('b/')]
    assert transform(['b', ' ']) == [Syllable('b/'), Syllable(' ')]
    assert transform(['b', 'ba']) == [Syllable('b='), Syllable('ba')]
# def test_transliterate_empty_string():
#     assert transliterate([]) == []


# def test_transliterate():
#     assert transliterate([' ']) == [' ']
#     assert transliterate(['a']) == ['A']
#     assert transliterate(['ba']) == ['b']
#     assert transliterate(['be']) == ['be']
#     assert transliterate(['b']) == ['b/']


# def test_transliterate_shorthand_j():
#     assert transliterate(['ja']) == ['D']
#     assert transliterate(['je']) == ['De']
#     assert transliterate(['j']) == ['D/']


# def test_transliterate_shorthand_ñ():
#     assert transliterate(['ña']) == ['~']
#     assert transliterate(['ñe']) == ['~e']
#     assert transliterate(['ñ']) == ['~/']


# def test_transliterate_shorthand_ng():
#     assert transliterate(['nga']) == ['N']
#     assert transliterate(['nge']) == ['Ne']
#     assert transliterate(['ng']) == ['N/']


# def test_transliterate_shorthand_ts():
#     assert transliterate(['tsa']) == ['C']
#     assert transliterate(['tse']) == ['Ce']
#     assert transliterate(['ts']) == ['C/']


# def test_transliterate_multiple_syllables():
#     assert transliterate(['a', 'ba']) == ['A', 'b']

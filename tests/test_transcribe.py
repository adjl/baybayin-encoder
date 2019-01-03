from app.app import translate
from app.char import Syllable


def test_transcribe():
    assert Syllable(' ').transcribe() == ' '

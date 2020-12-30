from unittest.mock import Mock
from io import StringIO

import pytest
import speech_recognition as sr

from app.subsystem.listener.engine import Engine


def test_invalid_engine():
    with pytest.raises(ValueError):
        Engine("blah", {})


def test_recognize():
    test_text = "this is a test"
    options = {"option1": "option_value", "option2": "other_option_value"}
    engine = Engine("google", options)
    audio = sr.AudioFile(StringIO("test"))
    engine.recognize_google = Mock(return_value=test_text)
    s = engine.recognize(audio)
    assert s == test_text

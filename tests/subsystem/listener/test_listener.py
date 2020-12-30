from unittest.mock import Mock, patch
from io import StringIO

import speech_recognition as sr
import pytest

from app.subsystem.listener.listener import Listener


def test_listen_for_duration():
    duration = 10
    message_bus = Mock()
    engine = Mock()
    audio_file = sr.AudioFile("test")
    engine.record.return_value = audio_file
    mic = Mock()
    listener = Listener(message_bus, engine, mic)
    return_value = listener.listen_for_duration(duration)
    engine.record.assert_called_once_with(source=mic, duration=duration)
    assert type(audio_file) == sr.AudioFile
    assert return_value == audio_file


@pytest.mark.timeout(1)
def test_listen_for_phrase():
    test_phrase = "this is a test"
    message_bus = Mock()
    engine = Mock()
    audio_file = StringIO("test")
    engine.listen.side_effect = [sr.WaitTimeoutError, audio_file, audio_file]
    engine.recognize.side_effect = [sr.UnknownValueError, test_phrase]
    mic = Mock()
    listener = Listener(message_bus, engine, mic)
    return_value = listener.listen_for_phrase()
    engine.listen.assert_called()
    engine.recognize.assert_called()
    assert return_value == test_phrase


@pytest.mark.timeout(1)
def test_wait_for_wake_word():
    non_wake_word = "apples"
    wake_word = "beezlebub"
    message_bus = Mock()
    engine = Mock()
    audio_file = StringIO("test")
    engine.listen.side_effect = [audio_file, audio_file]
    engine.recognize.side_effect = [non_wake_word, wake_word]
    mic = Mock()
    listener = Listener(message_bus, engine, mic)
    listener.wait_for_wake_word(wake_word)
    engine.listen.assert_called()
    engine.recognize.assert_called()

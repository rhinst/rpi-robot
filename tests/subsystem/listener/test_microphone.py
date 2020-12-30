from unittest.mock import patch, Mock

import pytest
import speech_recognition as sr

from app.subsystem.listener.microphone import get_microphone_index, Microphone
from app.subsystem.listener.exception import DeviceNotFoundException


def test_get_microphone_index():
    device_name = "Fancy-Pants Microphone"
    microphones = [
        "Microphone Check 1",
        "Microphone Check 2",
        device_name,
        "Built-in garbage microphone",
    ]
    with patch(
        "app.subsystem.listener.microphone.sr.Microphone.list_microphone_names",
        Mock(return_value=microphones),
    ):
        index = get_microphone_index(device_name)
    assert index == 2


def test_get_nonexistent_microphone_index():
    device_name = "Fancy-Pants Microphone"
    microphones = [
        "Microphone Check 1",
        "Microphone Check 2",
        "Built-in garbage microphone",
    ]
    with patch(
        "app.subsystem.listener.microphone.sr.Microphone.list_microphone_names",
        Mock(return_value=microphones),
    ), pytest.raises(DeviceNotFoundException):
        index = get_microphone_index(device_name)


def test_create_microphone():
    device_name = "Fancy-Pants Microphone"
    microphones = [
        "Microphone Check 1",
        "Microphone Check 2",
        device_name,
        "Built-in garbage microphone",
    ]
    with patch(
        "app.subsystem.listener.microphone.sr.Microphone.list_microphone_names",
        Mock(return_value=microphones),
    ):
        mic = Microphone(device_name)
    assert isinstance(mic, sr.Microphone)

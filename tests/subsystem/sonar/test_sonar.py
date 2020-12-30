from unittest.mock import patch, Mock

from app.subsystem.sonar.sonar import Sonar
import app.subsystem.GPIO.mock as GPIO


def test_measure_distance():
    m_connection = Mock()
    trigger_pin = 1
    echo_pin = 2
    m_gpio = Mock()
    m_gpio.LOW = 0
    m_gpio.HIGH = 1
    m_gpio.input.side_effect = [GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW]
    m_time = Mock()
    m_time.time.side_effect = [1609256042, 1609256042.2, 1609256042.4, 1609256042.6]
    with patch("app.subsystem.sonar.sonar.GPIO", m_gpio), patch(
        "app.subsystem.sonar.sonar.time", m_time
    ):
        sonar = Sonar(m_connection, trigger_pin, echo_pin)
        sonar.measure_distance()
        distance = sonar.get_distance()
    assert distance == 6860.0

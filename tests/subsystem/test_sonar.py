from unittest.mock import patch, Mock

from app.subsystem.sonar.sonar import Sonar


def test_measure_distance():
    m_connection = Mock()
    trigger_pin = 1
    echo_pin = 2
    m_gpio = Mock()
    m_gpio.input.side_effects = [0, 1, 1, 0]
    m_time = Mock(side_effect=[1609256042, 1609256042.2, 1609256042.6])
    with patch("app.subsystem.sonar.sonar.GPIO", m_gpio), patch("app.subsystem.sonar.sonar.time.time", m_time):
        sonar = Sonar(m_connection, trigger_pin, echo_pin)
        sonar.measure_distance()
        distance = sonar.get_distance()
    assert distance == 3430.0

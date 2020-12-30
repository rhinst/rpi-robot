from unittest.mock import Mock, patch

import pytest

from app.controller.voice.controller import start_voice_controller


@pytest.mark.timeout(1)
def test_main_loop():
    m_message_bus = Mock()
    m_cycle = Mock(side_effect=[True, True, StopIteration])
    with patch("app.controller.voice.controller.itertools.cycle", m_cycle):
        try:
            start_voice_controller(m_message_bus)
        except StopIteration:
            pass
    m_cycle.assert_called()

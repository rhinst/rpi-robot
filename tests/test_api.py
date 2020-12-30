from unittest.mock import Mock, patch

import pytest

from app.api import start_api


@pytest.mark.timeout(1)
def test_main_loop():
    m_cycle = Mock(side_effect=[True, True, StopIteration])
    with patch("app.api.cycle", m_cycle):
        try:
            start_api(Mock())
        except StopIteration:
            pass
    m_cycle.assert_called()
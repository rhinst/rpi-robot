from unittest.mock import patch, Mock
import app.server


def test_run(test_config):
    with patch("app.server.load_config", Mock(return_value=test_config)):
        app.server.run()
    assert True

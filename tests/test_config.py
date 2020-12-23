from unittest.mock import patch, Mock
from app.config import load_config, get_config_path


def test_load_config(test_config):
    mock_config_path = "/test/path"
    mock_processor = Mock()
    mock_processor.return_value.process.return_value = test_config
    mock_get_config_path = Mock(return_value="/test/path")
    with patch("app.config.ConfigProcessor", new=mock_processor), patch(
        "app.config.get_config_path", mock_get_config_path
    ):
        config = load_config("test")
    assert mock_processor.process.called_once_with(path=mock_config_path)
    assert config == test_config

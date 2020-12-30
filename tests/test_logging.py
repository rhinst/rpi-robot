from unittest.mock import patch

from app.logging import initialize_logger


def test_initialize_logger(caplog):
    config = {"test": "option"}
    with patch("app.logging.dictConfig") as m_dict_config:
        initialize_logger(config)
        m_dict_config.assert_called_once_with(config)


from unittest.mock import patch, Mock

import pytest

from app.controller.cli.controller import start_cli_controller, process_input
from app.message_bus.message import CommandMessage


@pytest.mark.parametrize(
    "command,arguments",
    [
        ("drive", ["the", "bus"]),
        ("say", ['"goodnight Gracie"']),
        ("reboot", []),
    ],
)
def test_process_input(command, arguments):
    msg = process_input(" ".join([command] + arguments))
    assert msg == CommandMessage(
        channel="core.command",
        command=command,
        arguments=[argument.replace('"', "") for argument in arguments],
    )


def test_main_loop():
    command = "drive"
    arguments = ["the", "bus"]
    m_message_bus = Mock()
    m_cycle = Mock(side_effect=[True, True, StopIteration])
    m_input = Mock(side_effect=[" \n", " ".join([command] + arguments)])
    with patch("app.controller.cli.controller.cycle", m_cycle), patch(
        "builtins.input", m_input
    ):
        try:
            start_cli_controller(m_message_bus)
        except StopIteration:
            pass
    m_message_bus.publish.assert_called_once_with(
        CommandMessage(channel="core.command", command=command, arguments=arguments)
    )

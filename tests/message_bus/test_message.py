from app.message_bus.message import (
    Message,
    GenericMessage,
    CommandMessage,
    MessageFactory
)


def test_message_repr():
    msg = Message(channel="test.channel")
    assert repr(msg) is ""


def test_command_message_repr():
    command = "run"
    arguments = ["this", "thing"]
    msg = CommandMessage(
        channel="test.channel",
        command=command,
        arguments=arguments
    )
    assert repr(msg) == f"{command} {' '.join(arguments)}"


def test_generic_message_repr():
    data = "This is a test"
    msg = GenericMessage(
        channel="test.channel",
        data=data
    )
    assert repr(msg) == data


def test_message_factory_command_message():
    factory = MessageFactory()
    redis_msg = {
        "pattern": None,
        "channel": bytes("core.command", "utf-8"),
        "data": bytes("This is a test", "utf-8"),
        "type": "message"
    }
    msg = factory.from_redis_msg(redis_msg)
    assert type(msg) == CommandMessage
    assert msg.channel == redis_msg['channel'].decode("utf-8")
    assert redis_msg['data'].decode('utf-8') == f"{msg.command} {' '.join(msg.arguments)}"


def test_message_factory_unknown():
    factory = MessageFactory()
    redis_msg = {
        "pattern": None,
        "channel": bytes("unknown.channel", "utf-8"),
        "data": bytes("This is a test", "utf-8"),
        "type": "message"
    }
    msg = factory.from_redis_msg(redis_msg)
    assert type(msg) == GenericMessage
    assert msg.channel == redis_msg['channel'].decode("utf-8")
    assert redis_msg['data'] == redis_msg['data']

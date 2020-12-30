from unittest.mock import Mock, patch

from app.message_bus.connection import Connection, ConnectionPool
from app.message_bus.message import GenericMessage


def test_get_connection():
    m_redis = Mock()
    with patch("app.message_bus.connection.RedisConnectionPool"), patch(
        "app.message_bus.connection.Redis", new=Mock(return_value=m_redis)
    ):
        pool = ConnectionPool("localhost", 1234)
        connection = pool.get_connection()
    assert type(connection) == Connection
    m_redis.pubsub.assert_called_once()


def test_subscribe_one_channel():
    m_redis = Mock()
    m_pubsub = Mock()
    connection = Connection(m_redis, m_pubsub)
    connection.subscribe("test.channel")
    m_pubsub.subscribe.assert_called_once_with("test.channel")


def test_subscribe_multiple_channels():
    m_redis = Mock()
    m_pubsub = Mock()
    connection = Connection(m_redis, m_pubsub)
    connection.subscribe("test.channel1", "test.channel2")
    m_pubsub.subscribe.assert_called_once_with("test.channel1", "test.channel2")


def test_unsubscribe_one_channel():
    m_redis = Mock()
    m_pubsub = Mock()
    connection = Connection(m_redis, m_pubsub)
    connection.unsubscribe("test.channel1")
    m_pubsub.unsubscribe.assert_called_once_with("test.channel1")


def test_unsubscribe_multiple_channels():
    m_redis = Mock()
    m_pubsub = Mock()
    connection = Connection(m_redis, m_pubsub)
    connection.unsubscribe("test.channel1", "test.channel2")
    m_pubsub.unsubscribe.assert_called_once_with("test.channel1", "test.channel2")


def test_publish():
    data = "This is a test"
    message = GenericMessage(channel="test.channel", data=data)
    m_redis = Mock()
    m_pubsub = Mock()
    connection = Connection(m_redis, m_pubsub)
    connection.publish(message)
    m_redis.publish.assert_called_once_with("test.channel", data)


def test_get_message():
    redis_msg = {
        "pattern": None,
        "type": "message",
        "channel": "test.channel",
        "data": "test data",
    }
    m_redis = Mock()
    m_pubsub = Mock()
    m_pubsub.get_message.return_value = redis_msg
    connection = Connection(m_redis, m_pubsub)
    with patch("app.message_bus.connection.MessageFactory") as m_msg_factory:
        m_msg_factory.from_redis_msg.return_value = GenericMessage(
            channel=redis_msg["channel"], data=redis_msg["data"]
        )
        message = connection.get_message()
    m_msg_factory.from_redis_msg.assert_called_once_with(redis_msg)
    assert type(message) == GenericMessage
    assert message.channel == redis_msg["channel"]
    assert message.data == redis_msg["data"]


def test_get_message_none():
    m_redis = Mock()
    m_pubsub = Mock()
    m_pubsub.get_message.return_value = None
    connection = Connection(m_redis, m_pubsub)
    message = connection.get_message()
    assert message is None

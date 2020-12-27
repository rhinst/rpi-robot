from typing import Union

from redis import ConnectionPool as RedisConnectionPool, Redis
from redis.client import PubSub

from app.message_bus.message import Message, MessageFactory


class ConnectionPool:
    pool: RedisConnectionPool

    def __init__(self, host: str, port: int):
        self.pool = RedisConnectionPool(host=host, port=port, db=0)

    def get_connection(self):
        pub_client = Redis(connection_pool=self.pool)
        sub_client = pub_client.pubsub()
        return Connection(pub_client, sub_client)


class Connection:
    pub_client: Redis
    sub_client: PubSub

    def __init__(self, pub_client: Redis, sub_client: PubSub):
        self.pub_client = pub_client
        self.sub_client = sub_client

    def subscribe(self, *channels: str):
        self.sub_client.subscribe(*channels)

    def unsubscribe(self, *channels: str):
        self.sub_client.unsubscribe(*channels)

    def publish(self, message: Message):
        self.pub_client.publish(message.channel, repr(message))

    def get_message(self) -> Union[None, Message]:
        if redis_msg := self.sub_client.get_message(ignore_subscribe_messages=True):
            return MessageFactory.from_redis_msg(redis_msg)
        return None

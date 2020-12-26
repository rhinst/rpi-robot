import redis
from app.message_bus.message import Message


class ConnectionPool:
    pool: redis.ConnectionPool

    def __init__(self, host: str, port: int):
        self.pool = redis.ConnectionPool(host=host, port=port, db=0)

    def get_connection(self):
        return redis.Redis(connection_pool=self.pool)


class Connection:
    pub_client: redis.Redis
    sub_client: redis.client.PubSub

    def subscribe(self, *channels: str):
        self.sub_client.subscribe(*channels)

    def unsubscribe(self, *channels: str):
        self.sub_client.unsubscribe(*channels)

    def publish(self, message: Message):
        self.pub_client.publish(message.channel, message.data)

    def get_message(self) -> Message:
        redis_msg = self.sub_client.get_message(ignore_subscribe_messages=True)
        return Message(
            channel=redis_msg['channel'],
            data=redis_msg['data']
        )

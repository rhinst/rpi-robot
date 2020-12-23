from typing import Dict, List, Any
from dataclasses import dataclass

from app.logging import logger


class ChannelNotFoundException(Exception):
    pass


@dataclass
class Message:
    channel: str
    data: Any


class Channel:
    name: str
    subscribers: List

    def __init__(self, name: str):
        self.name = name
        self.subscribers = []

    def subscribe(self, subscriber):
        logger.debug("Adding a subscriber to %s: %s", self.name, subscriber.__class__.__name__)
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        logger.debug("Removing a subscriber from %s: %s", self.name, subscriber.__class__.__name__)
        self.subscribers.remove(subscriber)

    def is_subscribed(self, subscriber):
        return subscriber in self.subscribers

    def publish(self, data: Any):
        logger.debug("Sending message to all subscribers")
        for subscriber in self.subscribers:
            logger.debug("Sending message to subcriber: %s", subscriber.__class__.__name__)
            subscriber.receive_message(Message(channel=self.name, data=data))


class MessageBus:
    channels: Dict[str, Channel]

    def __init__(self):
        self.channels = {}

    def subscribe(self, subscriber, *channels: str):
        logger.debug("Subscriber '%s' requested a subscription to %s", subscriber.__class__.__name__, ", ".join(channels))
        for channel in channels:
            if channel not in self.channels:
                self.create_channel(channel)
            self.channels[channel].subscribe(subscriber)

    def unsubscribe(self, subscriber, *channels: str):
        logger.debug("Subscriber '%s' requested unsubscription from %s", subscriber.__class__.__name__, ", ".join(channels))
        for channel in channels:
            if channel not in self.channels:
                raise ChannelNotFoundException("Channel not found")
            self.channels[channel].unsubscribe(subscriber)

    def publish(self, channel: str, data: Any):
        logger.debug("Publishing a message to %s:", channel)
        logger.debug(str(data))
        if channel not in self.channels:
            self.create_channel(channel)
        self.channels[channel].publish(data)

    def create_channel(self, channel: str):
        if channel not in self.channels:
            self.channels[channel] = Channel(channel)

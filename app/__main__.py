import os
import threading

from app.logging import initialize_logger, logger
from app.config import load_config
from app.api import start_api
from app.controller.cli.controller import start_cli_controller
from app.controller.voice.controller import start_voice_controller
from app.message_bus import ConnectionPool
from app.subsystem.speech.talker import Talker
from app.subsystem.motor.driver import Driver, MotorPins
from app.subsystem.sonar import Sonar


def main():
    env = os.getenv("ENVIRONMENT", "dev")
    config = load_config(env)
    initialize_logger(config["logging"])
    redis_host = config["message_bus"]["host"]
    redis_port = int(config["message_bus"]["port"])
    pool = ConnectionPool(host=redis_host, port=redis_port)
    logger.info("Starting Subsystems")
    speech_subsystem = Talker(message_bus=pool.get_connection())
    speech_subsystem.start()
    pins = MotorPins(
        front_left_dir=config["subsystems"]["motor"]["gpio_pins"]["front_left"][
            "direction"
        ],
        front_left_speed=config["subsystems"]["motor"]["gpio_pins"]["front_left"][
            "speed"
        ],
        front_right_dir=config["subsystems"]["motor"]["gpio_pins"]["front_right"][
            "direction"
        ],
        front_right_speed=config["subsystems"]["motor"]["gpio_pins"]["front_right"][
            "speed"
        ],
        rear_left_dir=config["subsystems"]["motor"]["gpio_pins"]["rear_left"][
            "direction"
        ],
        rear_left_speed=config["subsystems"]["motor"]["gpio_pins"]["rear_left"][
            "speed"
        ],
        rear_right_dir=config["subsystems"]["motor"]["gpio_pins"]["rear_right"][
            "direction"
        ],
        rear_right_speed=config["subsystems"]["motor"]["gpio_pins"]["rear_right"][
            "speed"
        ],
    )
    motor_subsystem = Driver(pool.get_connection(), pins)
    motor_subsystem.start()
    sonar_subsystem = Sonar(
        pool.get_connection(),
        config["subsystems"]["sonar"]["trigger_pin"],
        config["subsystems"]["sonar"]["echo_pin"],
    )
    sonar_subsystem.start()
    logger.info("Starting API")
    api = threading.Thread(target=start_api, args=(pool.get_connection(),))
    api.start()
    logger.info("Starting Voice Controller")
    voice = threading.Thread(
        target=start_voice_controller, args=(pool.get_connection(),)
    )
    voice.start()
    logger.info("Starting CLI")
    cli = threading.Thread(target=start_cli_controller, args=(pool.get_connection(),))
    cli.start()


if __name__ == "__main__":
    main()

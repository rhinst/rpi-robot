import os
from app.logging import initialize_logger, logger
from app.config import load_config
from app.api import Api
from app.controller import CliController, VoiceController
from app.message_bus import ConnectionPool


def main():
    env = os.getenv("ENVIRONMENT", "dev")
    config = load_config(env)
    initialize_logger(config["logging"])
    redis_host = config['message_bus']['host']
    redis_port = int(config['message_bus']['port'])
    pool = ConnectionPool(host=redis_host, port=redis_port)
    logger.info("Starting API")
    api = Api(pool.get_connection())
    api.start()
    logger.info("Starting Voice Controller")
    voice = VoiceController(pool.get_connection())
    voice.start()
    logger.info("Starting CLI")
    cli = CliController(pool.get_connection())
    cli.start()



if __name__ == "__main__":
    main()

import os
from app.server import RobotServer
from app.logging import initialize_logger
from app.config import load_config

if __name__ == "__main__":
    env = os.getenv("ENVIRONMENT", "dev")
    config = load_config(env)
    initialize_logger(config["logging"])
    server = RobotServer(config)
    server.start()

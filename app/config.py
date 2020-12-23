from himl import ConfigProcessor
import os


def get_config_path(env: str) -> str:
    return os.path.abspath(
        os.path.dirname(os.path.abspath(__file__)) + f"/../config/{env}"
    )


def load_config(env: str = "dev"):
    processor = ConfigProcessor()
    config_path = get_config_path(env)
    return processor.process(path=config_path)

from pytest import fixture


@fixture
def test_config():
    return {"logging": {"version": 1, "loggers": {"robot": {}}}}

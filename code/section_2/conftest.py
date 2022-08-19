from pytest import fixture

from config import Config

# This file is a place to put fixtures
# Anything in this directory or below has access to what's in where

# parser exists by default, it's just there when we use pytest so we can call it without imports
def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Environment to run test against")


@fixture(scope="session")
# request is just something native to pytest, more later
def env(request):
    # create an argument you can pass options to
    return request.config.getoption("--env")


# a fixture can use a fixture!
@fixture(scope="session")
def app_config(env):
    cfg = Config(env)
    return cfg

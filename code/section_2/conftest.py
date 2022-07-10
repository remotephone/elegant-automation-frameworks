# This file is a place to put fixtures
# Anything in this directory or below has access to what's in where

# parser exists by default, it's just there when we use pytest
def pytest_addoption(parser):
    parser.addoptionm("--env", action="store", )

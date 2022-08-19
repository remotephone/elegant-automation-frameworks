from pytest import fixture
from selenium import webdriver
import json


data_path = "test_data.json"


def load_test_data(path):
    with open(path) as data_file:
        data = json.load(data_file)
    return data


# I Got stuck trying to pass multiple options to each driver, this was tough in WSL
@fixture(params=[webdriver.Chrome, webdriver.Firefox, webdriver.Edge])
def browser(request):
    driver = request.param
    drvr = driver()
    # We need to shut it down when its done
    yield drvr
    drvr.quit()


@fixture(params=load_test_data(data_path))
def tv_brand(request):
    data = request.param
    return data

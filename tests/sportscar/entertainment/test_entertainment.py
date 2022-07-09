from selenium import webdriver
from pytest import mark

@mark.entertainment
def test_entertainment_functions_as_expected():
    assert True


@mark.ui
@mark.entertainment
def test_can_navigate_to_entertainment_page(chrome_browser):
    chrome_browser.get('http://www.siriusxm.com/')
    assert True
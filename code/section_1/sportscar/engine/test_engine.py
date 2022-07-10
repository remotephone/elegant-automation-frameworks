from selenium import webdriver

from pytest import mark

@mark.smoke
@mark.engine 
@mark.ui
def test_engine_functions_as_expected(chrome_browser):
    chrome_browser.get('http://www.artofmanliness.com/')
    assert True


from selenium import webdriver

from pytest import mark

@mark.smoke
@mark.engine 
@mark.ui
def test_engine_functions_as_expected():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('http://www.artofmanliness.com/')
    assert True


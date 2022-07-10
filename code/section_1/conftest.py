from pytest import fixture

from selenium import webdriver

@fixture(scope='function')
def chrome_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    return browser


@fixture(scope='function')
def chrome_browser_with_yield():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    yield browser
    print('everything after yield is teardown code!')



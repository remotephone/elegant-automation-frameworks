# Intro

## Setup

Install Pytest

`pipenv install pytest` - probably

### Install Selenium and Chrome and Chrome WebDriver

I seem to like to make things harder for myself, so I am doing this in Windows Subsystem for Linux instead of on Windows or a native OS. this breaks a few of the steps provided by the author.

This guide worked - <https://cloudbytes.dev/snippets/run-selenium-and-chrome-on-wsl2>

```bash
## Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install
chrome_driver=$(curl "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
echo "$chrome_driver"
curl -Lo chromedriver_linux64.zip "https://chromedriver.storage.googleapis.com/\
${chrome_driver}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo mnv chromedrive /usr/bin/chromedriver
rm *.zip
```

I also had to modify the chromedriver fixture. This is an example of a working function

```python
def test_engine_functions_as_expected():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=chrome_options)
    browser.get('http://www.artofmanliness.com/')
    assert True
```

## pytest.ini

see pytest.ini, `[pytest]` starts the file. We can usually get away with a minimum of 3 configurations, what you test files look like, what the test functions look like, and what the classes should look like.

## Markers

delineate tests so we know what we want to run when

```python
from pytest import mark

@mark.engine 
def test_engine_functions_as_expected():
    assert True

```

Test only the tests you want to test with `pytest -m engine`. Document the ones you want to use and expose to other people in your pytest.ini file

## Smoke testing

Bare minimum tests to be sure the whole thing won't blow up. You can mark it a smoke test.

You can run smoke and engine tests with `pytest -m "smoke or engine"`.

## Classes to group tests

simplifies grouping tests together. You can add functions really easy, mark it once, boom it all runs (see [body tests](../code/section_1/sportscar/body/test_body.py))

## Fixtures

Any fixture created in conftest.py is accessible to any directory its in and anything under it! Just put it at the root of your tests folder

You don't have to import them either! Pytest does the magic.

### Fixture Setup

1. Create them in your `conftest.py` - There's a working example in this repo.
2. Create your function and import what you need
3. Make sure it returns what you want.
4. Modify your test function to take the fixture as an argument

```py title="conftest.py"
# conftest.py
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
```

```py
#my test
@mark.ui
@mark.entertainment
def test_can_navigate_to_entertainment_page(chrome_browser):
    chrome_browser.get('http://www.siriusxm.com/')
    assert True
```

## Reporting

This section does not spark joy for me. Convert it to html or convert it to something jenkins can read.

```py
sudo apt install lynx
pytest --html="results.html"
lynx results.html
```

Also export with `pytest --junitxml="results.xml"`


----
There's an arbitrary split here in my notes, section_2 code begins here. 
----
## Customizing Test Runs with CLI and Config files
